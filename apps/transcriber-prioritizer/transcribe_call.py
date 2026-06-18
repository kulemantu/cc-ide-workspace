#!/usr/bin/env python3
"""transcribe_call — .mov -> speaker-labelled transcript -> kick-off notes, via OpenRouter.

Pipeline:
  1. extract   ffmpeg: .mov -> mono mp3 (drops video, halves channels)
  2. transcribe  OpenRouter chat-completions + input_audio -> Gemini 2.5 -> diarized transcript
  3. notes      OpenRouter chat-completions -> structured kick-off notes from the transcript

Speaker diarization is model-inferred by Gemini (labels A/B/C + approx timestamps),
not acoustic. Good for short multi-party calls; not a substitute for a dedicated
diarization ASR when label precision is critical.

The API key is read from OPENROUTER_API_KEY only — never passed on argv (secrets hygiene).
Stdlib + ffmpeg only; no pip install required.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSION = "1.0.0"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# google/gemini-2.5-flash = fast + cheap, solid for short calls.
# google/gemini-2.5-pro   = more accurate attribution/synthesis, slower + pricier.
DEFAULT_TRANSCRIBE_MODEL = "google/gemini-2.5-flash"
DEFAULT_NOTES_MODEL = "google/gemini-2.5-pro"

DIARIZE_PROMPT = """You are a meticulous transcriptionist. Transcribe this audio of a project kick-off call into a SPEAKER-LABELLED transcript.

Rules:
- Identify each distinct speaker and label them consistently as "Speaker 1", "Speaker 2", etc.
- If speakers address each other by name during the call (e.g. "Thanks, Sarah", "Over to you, James"), infer and use those REAL names instead of "Speaker N", and keep each person's name consistent for the whole transcript. Only do this when you are confident from context; otherwise keep the generic label.
- Prefix every turn with an approximate timestamp [mm:ss] of when it starts.
- Transcribe verbatim — keep filler, hedges, and disagreements intact. Do NOT summarise or clean up.
- Use a new line per speaker turn. When a new speaker starts, emit a new labelled line.
- If two people talk over each other, note it as "[crosstalk]" and attribute your best guess.
- Do not invent content. If a stretch is inaudible, write "[inaudible]".

Output ONLY the transcript, no preamble.{speaker_hint}"""

NOTES_PROMPT = """You are a senior program manager writing the canonical record of a project KICK-OFF call.
The call has a DEFINED UNDERSTANDING (agreed scope/goals) but a LOT of feedback from DIFFERENT PARTIES.
Your job is to make the who-said-what legible and to separate settled decisions from open tension.

Input is a speaker-labelled transcript. Produce Markdown notes with EXACTLY these sections:

## TL;DR
3-5 bullets: what this project is, who's involved, and the single most important takeaway.

## The Defined Understanding
The scope/goals/approach that parties appear to AGREE on. State it as settled fact. If something is presented as agreed but a party pushed back, do not list it here — put it under Divergence.

## Feedback by Party
One subsection per speaker/stakeholder (use their label or name). Under each, bullet THEIR specific asks, concerns, and positions. Attribute precisely — do not blend parties.

## Alignment vs. Divergence
- **Aligned on:** points multiple parties endorsed.
- **Diverging on:** points where parties disagreed or pulled in different directions. Name who's on which side and what the tension is. This is the most important section — be specific, do not soften real disagreement.

## Decisions Made
Only things explicitly decided/agreed on the call. If none, say "No firm decisions — see Open Questions."

## Open Questions
Unresolved items, with who raised them.

## Action Items
A table: | Owner | Action | Due / trigger |. Owner = the named person responsible; "Unassigned" if not stated. Only include items someone actually committed to or was asked to do.

## Risks & Unknowns
Things that could derail delivery, including anything implied but not said aloud.

Be faithful to the transcript. Do not invent owners, dates, or decisions. Where the transcript is ambiguous about attribution, say so rather than guessing.{speaker_hint}"""


# ---------- pure helpers ----------

def speaker_hint_block(speakers: str | None) -> str:
    """Render an optional participant-roster hint appended to a prompt."""
    if not speakers:
        return ""
    return (
        "\n\nKnown participants (map speaker labels to these where confident): "
        + speakers
    )


def build_transcribe_payload(audio_b64: str, fmt: str, model: str,
                             speakers: str | None, max_tokens: int) -> dict:
    """Chat-completions payload carrying base64 audio for diarized transcription."""
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text",
                 "text": DIARIZE_PROMPT.format(speaker_hint=speaker_hint_block(speakers))},
                {"type": "input_audio",
                 "input_audio": {"data": audio_b64, "format": fmt}},
            ],
        }],
    }


def build_notes_payload(transcript: str, model: str,
                        speakers: str | None, max_tokens: int) -> dict:
    """Chat-completions payload turning a transcript into structured kick-off notes."""
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system",
             "content": NOTES_PROMPT.format(speaker_hint=speaker_hint_block(speakers))},
            {"role": "user",
             "content": "Here is the speaker-labelled transcript:\n\n" + transcript},
        ],
    }


def extract_message_text(response: dict) -> str:
    """Pull the assistant text out of an OpenRouter chat-completions response."""
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(
            f"unexpected OpenRouter response shape: {json.dumps(response)[:500]}"
        ) from exc


# Highest-to-lowest mono-mp3 bitrates we'll consider for speech.
BITRATE_LADDER_KBPS = [64, 48, 32, 24, 16]
# Keep the base64 request payload under this; Gemini's inline-audio cap is ~20 MB.
PAYLOAD_CAP_MB = 18.0


def choose_bitrate(duration_s: float, cap_payload_mb: float = PAYLOAD_CAP_MB) -> str:
    """Pick the best mono-mp3 bitrate that keeps the base64 payload under the cap.

    base64 inflates bytes by 4/3, so allowed mp3 bytes = cap * 3/4, and
    kbps = mp3_bytes * 8 / seconds / 1000. Returns the highest ladder rung that
    fits; floors at the lowest rung (caller should warn that chunking is needed).
    """
    if duration_s <= 0:
        return f"{BITRATE_LADDER_KBPS[0]}k"  # unknown duration -> safe default
    allowed_mp3_bytes = cap_payload_mb * 1e6 * 3 / 4
    max_kbps = allowed_mp3_bytes * 8 / duration_s / 1000
    for kbps in BITRATE_LADDER_KBPS:
        if kbps <= max_kbps:
            return f"{kbps}k"
    return f"{BITRATE_LADDER_KBPS[-1]}k"


def payload_exceeds_cap(duration_s: float, kbps: int,
                       cap_payload_mb: float = PAYLOAD_CAP_MB) -> bool:
    """True if even `kbps` won't fit under the cap for this duration (needs chunking)."""
    mp3_bytes = kbps * 1000 / 8 * duration_s
    return mp3_bytes * 4 / 3 > cap_payload_mb * 1e6


# ---------- side-effecting wrappers ----------

def extract_audio(mov_path: Path, out_path: Path, bitrate: str = "64k") -> Path:
    """ffmpeg: video file -> mono mp3 at the given bitrate. Returns out_path."""
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(mov_path),
         "-vn", "-ac", "1", "-c:a", "libmp3lame", "-b:a", bitrate, str(out_path)],
        check=True, capture_output=True,
    )
    return out_path


def b64_of(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def probe_duration(path: Path) -> float:
    """Audio/video duration in seconds via ffprobe (0.0 if it can't be read)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def resolve_bitrate(args, src: Path) -> str:
    """Honor an explicit --bitrate; otherwise pick one adaptively from duration."""
    if args.bitrate != "auto":
        return args.bitrate
    dur = probe_duration(src)
    kbps = int(choose_bitrate(dur).rstrip("k"))
    if payload_exceeds_cap(dur, kbps):
        print(f"[warn] {dur/60:.0f}-min audio exceeds the single-request payload cap "
              f"even at {kbps}k. Sending anyway; if it fails, chunking is needed "
              f"(see README roadmap).", file=sys.stderr)
    return f"{kbps}k"


def post_openrouter(payload: dict, api_key: str) -> dict:
    """POST a chat-completions request to OpenRouter, return parsed JSON."""
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost/transcribe_call",
            "X-Title": "kickoff-transcribe",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=1800) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {body[:500]}") from exc


def require_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Error: OPENROUTER_API_KEY not set. "
                 "Run:  ! read -s k && export OPENROUTER_API_KEY=$k")
    return key


def need_input(args) -> Path:
    """The --input path, or a clear error when a command needs it but it's absent."""
    if args.input is None:
        sys.exit("Error: --input <file> is required for this command "
                 "(or pass the relevant --audio/--transcript override).")
    return args.input


# ---------- commands ----------

def cmd_extract(args) -> dict:
    out = args.audio or need_input(args).with_suffix(".mp3")
    bitrate = resolve_bitrate(args, need_input(args))
    extract_audio(need_input(args), out, bitrate)
    size_mb = out.stat().st_size / 1e6
    return {"audio": str(out), "size_mb": round(size_mb, 2), "bitrate": bitrate}


def cmd_transcribe(args) -> dict:
    key = require_key()
    audio = args.audio or need_input(args).with_suffix(".mp3")
    if not audio.exists():
        extract_audio(need_input(args), audio, resolve_bitrate(args, need_input(args)))
    payload = build_transcribe_payload(
        b64_of(audio), audio.suffix.lstrip("."), args.model,
        args.speakers, args.max_tokens)
    transcript = extract_message_text(post_openrouter(payload, key))
    out = args.transcript or need_input(args).with_suffix(".transcript.md")
    out.write_text(transcript)
    return {"transcript": str(out), "chars": len(transcript), "model": args.model}


def cmd_notes(args) -> dict:
    key = require_key()
    src = args.transcript or need_input(args).with_suffix(".transcript.md")
    if not src.exists():
        sys.exit(f"Error: transcript not found at {src}. Run 'transcribe' first.")
    payload = build_notes_payload(
        src.read_text(), args.notes_model, args.speakers, args.max_tokens)
    notes = extract_message_text(post_openrouter(payload, key))
    out = args.notes or need_input(args).with_suffix(".notes.md")
    out.write_text(notes)
    return {"notes": str(out), "chars": len(notes), "model": args.notes_model}


def cmd_all(args) -> dict:
    return {
        "extract": cmd_extract(args),
        "transcribe": cmd_transcribe(args),
        "notes": cmd_notes(args),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="transcribe_call", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"transcribe_call {VERSION}")
    p.add_argument("command", nargs="?", default="all",
                   choices=["all", "extract", "transcribe", "notes"],
                   help="all (default) | extract | transcribe | notes")
    p.add_argument("--input", type=Path,
                   help="source video/audio file (required unless --audio/--transcript given)")
    p.add_argument("--audio", type=Path, help="audio path [default: <input>.mp3]")
    p.add_argument("--transcript", type=Path,
                   help="transcript path [default: <input>.transcript.md]")
    p.add_argument("--notes", type=Path,
                   help="notes path [default: <input>.notes.md]")
    p.add_argument("--model", default=DEFAULT_TRANSCRIBE_MODEL,
                   help=f"diarization model [default: {DEFAULT_TRANSCRIBE_MODEL}]")
    p.add_argument("--notes-model", default=DEFAULT_NOTES_MODEL,
                   help=f"notes model [default: {DEFAULT_NOTES_MODEL}]")
    p.add_argument("--speakers",
                   help='participant roster hint, e.g. "Alice (PM), Bob (eng), Carol (client)"')
    p.add_argument("--bitrate", default="auto",
                   help="mp3 bitrate, or 'auto' to size it to fit the request cap [default: auto]")
    p.add_argument("--max-tokens", type=int, default=16384)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    dispatch = {"all": cmd_all, "extract": cmd_extract,
                "transcribe": cmd_transcribe, "notes": cmd_notes}
    try:
        data = dispatch[args.command](args)
    except Exception as exc:  # noqa: BLE001 — surface as actionable envelope
        if args.json:
            print(json.dumps({"ok": False, "data": {"error": str(exc)}}))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"ok": True, "data": data}))
    else:
        print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
