# transcriber-prioritizer

Turn a call recording into a **speaker-labelled transcript** and then into
**structured, prioritized notes** — via OpenRouter, no local model.

Built for multi-party calls (kick-offs, stakeholder reviews) where *who said
what* matters: the notes separate the settled "defined understanding" from
multi-party feedback, alignment vs. divergence, decisions, open questions, and
owned action items.

## How it works

```
.mov/.mp4/.m4a  ──ffmpeg──▶  mono mp3  ──OpenRouter──▶  diarized transcript  ──OpenRouter──▶  notes.md
                                          (Gemini 2.5,                         (Gemini 2.5 Pro,
                                           input_audio)                         synthesis)
```

Diarization is **model-inferred** by Gemini (speaker labels + approximate
timestamps; real names substituted when speakers address each other by name) —
not acoustic. Great for short multi-party calls; not a substitute for a
dedicated diarization ASR (AssemblyAI/Deepgram) when label precision is
critical. See the docstring in `transcribe_call.py` for the full rationale.

## Requirements

- `ffmpeg` on PATH
- Python 3 (stdlib only — no `pip install`)
- `OPENROUTER_API_KEY` in the environment (never passed on argv)

> Stdlib-only + `unittest` is a deliberate divergence from the workspace
> `uv`/`ruff`/`pyright` default, so this tool runs on any box with `python3` +
> `ffmpeg`. See `docs/pattern-apps.md` › *Tooling carve-out*.

## Setup

```bash
cp .env.example .env          # then put your OpenRouter key in .env
set -a; . .env; set +a        # load OPENROUTER_API_KEY into the environment
```

`.env` is gitignored; `.env.example` is the committed template.

## Usage

```bash
# Whole pipeline (extract → diarize → notes)
python3 transcribe_call.py all --input /path/to/call.mov --model google/gemini-2.5-pro --json

# Individual steps
python3 transcribe_call.py extract    --input call.mov
python3 transcribe_call.py transcribe --input call.mov --model google/gemini-2.5-pro
python3 transcribe_call.py notes      --transcript call.transcript.md

# Help / all flags
python3 transcribe_call.py --help
```

Outputs land next to the input: `<file>.mp3`, `<file>.transcript.md`,
`<file>.notes.md` (all gitignored at the repo root).

Optional `--speakers "Alice (PM), Bob (eng), Carol (client)"` feeds a roster
hint to improve attribution.

## Tests

```bash
python3 -m unittest test_transcribe_call -v
```

## Roadmap (future — not yet built)

This started life as a one-file helper (`transcribe_call.py`). The intent is to
grow it into a proper CLI:

- [ ] Rename entry point + package layout (`script_meta.py` + `cli.py` per the
      workspace CLI conventions: `--help`, `info --json`, `check --json`).
- [ ] `category:action` subcommands (e.g. `transcribe:run`, `notes:run`,
      `notes:prioritize`).
- [ ] Chunking for long recordings (>~30 min) that exceed single-request audio
      size limits — auto-split + stitch.
- [ ] The "prioritizer" half: rank action items / feedback by urgency & owner,
      emit a machine-readable task list (`--json`) for downstream tools.
- [ ] Pluggable transcript backend (OpenRouter audio-chat vs. a real
      diarization ASR) behind one flag.
