---
paths:
  - "**/*"
---

# Scripting Philosophy: Do It, Then Tool It, Then Script It

Scripts are a last resort. The default is to do the work directly — from model context or with a CLI tool. The workspace should be a log of learning and using tools, not a code factory.

## The Escalation Ladder

**Tier 0 — Model context.** If Claude can produce the output directly (write text, generate slide content, draft a document, create structured data), do it. No code needed.

**Tier 1 — Existing CLI tool.** If the task needs a tool the system already has (ffmpeg, curl, jq, pandoc, etc.), call it directly via Bash. One command, not a script.

**Tier 2 — New CLI tool.** If a CLI tool would handle it but isn't installed, suggest it to the user. Explain what it does, let them decide whether to install it. Use Claude Code to install and orchestrate it if approved. Examples: imagemagick for image manipulation, poppler-utils for PDF extraction, yt-dlp for video downloads.

**Tier 3 — Python script.** Only when:
- The task involves super-structured data (CSVs, databases, JSON pipelines) where a script genuinely adds value, OR
- Multiple tools/libraries need to be orchestrated together (e.g., video captioning: extract frames + OCR + transcribe + merge), OR
- The user has repeated the *same operation* 3+ times and automation is justified (see escalation below).

**Always ask the user before writing a script.** Even at Tier 3, propose the scripting approach and wait for approval. Do not default to "let me write a Python script for that."

## Routines: Tracking Repeated Operations

A **routine** is a recurring operation the user performs. Claude tracks routines in memory to detect repetition across sessions and escalate suggestions appropriately.

### The escalation cycle

| Occurrence | Action |
|-----------|--------|
| 1st time | Just do it (Tier 0 or Tier 1). Save a routine memory. |
| 2nd time | Do it, then mention: "If you do this often, there's [tool/library] that could handle it." Update the routine. |
| 3rd+ time | Suggest a script or CLI workflow, explain the tradeoff. Update the routine. |

### Routine memory format

Each routine is a memory file named `routine_<slug>.md`:

```markdown
---
name: <short name — e.g., "Audio trimming">
description: <one-line for matching — e.g., "User trims start/end of audio files">
type: project
---

**Operation:** <verb + object — e.g., "trim audio file">
**Input type:** <what kind of input — e.g., "podcast MP3/WAV files">
**Output:** <what gets produced — e.g., "trimmed audio file">
**Current tier:** <0|1|2|3>
**Tool/method used:** <how it was done — e.g., "ffmpeg CLI">

## Log
- YYYY-MM-DD: <what happened, what tier was used>

## Next escalation
<what to suggest next time — e.g., "suggest a wrapper script with presets">
```

### Cross-session tracking

Before starting any task, check memory for `routine_*` files with a matching operation/input type. A match means this isn't the first time — escalate accordingly. After completing a task, create or update the routine memory.

### What counts as "the same operation"

Same operation = same transformation on same type of input.
- Extracting text from a cheque image then another cheque image = same operation (OCR on documents)
- Generating a strategy deck then a team intro deck = NOT the same operation (different content/structure, just both .pptx)
- Trimming the intro off a podcast then trimming another podcast = same operation (audio trim)
- Trimming a podcast then extracting a clip from a video = related but different operations

The test: "Could a single script/command handle both instances with just different input files?" If yes, it's the same operation. If the script would need fundamentally different logic, it's not.

## What This Means in Practice

| Task | Wrong approach | Right approach |
|------|---------------|----------------|
| Trim 10s off an audio file | Write a Python script with pydub | `ffmpeg -i input.mp3 -ss 10 output.mp3` |
| Grayscale a photo | Write a Python script with Pillow | Suggest imagemagick: `convert input.jpg -colorspace Gray output.jpg` |
| Generate a slide deck | Write a Python script with python-pptx | Produce the content directly, or use a CLI presentation tool |
| Extract text from a PDF | Write a Python script with PyPDF2 | `pdftotext input.pdf output.txt` (poppler-utils) |
| Analyze a CSV with 50 columns | Call ffmpeg | Write a Python script with pandas — this is what scripts are for |
| Caption a video | One bash command | Write a Python script — multiple tools need orchestration |
