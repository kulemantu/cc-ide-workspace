---
description: Transcribe a call recording into diarized meeting notes with speaker attribution.
---

# /transcribe

Runs the transcriber-prioritizer app's full pipeline on a recording:
extract audio → diarize with speaker labels → synthesize structured notes.

## Parsing the user's args

The user provides a file path and optional flags after `/transcribe`. Parse these from the args string:

- **Required**: a path to a video/audio file (`.mov`, `.mp4`, `.m4a`, or any ffmpeg-compatible format)
- **Optional**: `--speakers "Name (role), Name (role)"` — improves speaker attribution
- **Optional**: `--model <model>` — override the transcription model (default: `google/gemini-2.5-flash`)
- **Optional**: `--notes-model <model>` — override the notes synthesis model (default: `google/gemini-2.5-pro`)

If the user provides no args, ask for the path to the recording.

## Prerequisites — check before running

Run these two checks. If either fails, guide the user through setup instead of running the pipeline.

### 1. OPENROUTER_API_KEY

```bash
echo "${OPENROUTER_API_KEY:+set}" || echo "not set"
```

If not set, tell the user:

> `OPENROUTER_API_KEY` is not set. To set it up:
>
> 1. Get an API key from [OpenRouter](https://openrouter.ai/keys)
> 2. Copy the template: `cp apps/transcriber-prioritizer/.env.example apps/transcriber-prioritizer/.env`
> 3. Add your key to the `.env` file
> 4. Load it: `set -a; . apps/transcriber-prioritizer/.env; set +a`
>
> See `apps/transcriber-prioritizer/README.md` for details.

Stop here — do not run the pipeline.

### 2. ffmpeg

```bash
which ffmpeg
```

If not found, tell the user to install it (`brew install ffmpeg` on macOS, `apt install ffmpeg` on Linux).

## Run the pipeline

Once prerequisites are verified:

```bash
uv run python3 apps/transcriber-prioritizer/transcribe_call.py all --input "<path>" [--speakers "<roster>"] [--model <model>] [--notes-model <model>]
```

This takes a while (1-5 minutes depending on recording length and model). Tell the user it's running.

## After

Report the three output files created next to the input:
- `<input>.mp3` — extracted mono audio
- `<input>.transcript.md` — diarized transcript with speaker labels and timestamps
- `<input>.notes.md` — structured meeting notes (TL;DR, feedback by party, action items, etc.)

Offer to read or summarize the notes file.
