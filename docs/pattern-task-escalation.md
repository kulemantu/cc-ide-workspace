# Pattern: Task Escalation

How Claude decides whether to handle a task directly, use a CLI tool, or write a script. The workspace is designed for learning and using tools — not for generating code at every opportunity.

## The escalation ladder

```
Tier 0: Model context     → Claude produces the output directly (text, slides, structured data)
Tier 1: Existing CLI tool  → One bash command (ffmpeg, curl, jq, pandoc)
Tier 2: New CLI tool       → Suggest installing a tool, user decides (imagemagick, poppler-utils, yt-dlp)
Tier 3: Python script      → Only for structured data, multi-tool orchestration, or proven repeated operations
```

The default is always the lowest tier that works. Scripts are a last resort, and even then Claude asks before writing one.

## When each tier applies

**Tier 0 — Model context** works when the task is about *content*, not *transformation*. Drafting a document, generating slide content, writing structured JSON, summarizing text. No code needed because the model *is* the tool.

**Tier 1 — Existing CLI tool** works when the system already has the right tool. Trimming audio with ffmpeg, converting formats with pandoc, querying JSON with jq. One command, not a script. The workspace becomes a log of learning these tools.

**Tier 2 — New CLI tool** works when a purpose-built tool exists but isn't installed. Claude explains what the tool does and lets the user decide. If approved, Claude installs it and runs it. Examples: imagemagick for image manipulation, poppler-utils for PDF text extraction, yt-dlp for video downloads. This teaches the user a new tool they can use independently.

**Tier 3 — Python script** works when:
- The task involves super-structured data (CSVs, databases, JSON pipelines)
- Multiple tools need to be orchestrated together (e.g., video captioning: extract frames + OCR + transcribe + merge)
- The user has repeated the same operation enough times that automation is justified

## Routines: tracking repeated operations

A **routine** is a recurring operation Claude tracks across sessions. When a task reaches Tier 0 or 1, Claude saves it as a routine in memory. On subsequent occurrences, Claude escalates its suggestion:

| Occurrence | What Claude does |
|-----------|-----------------|
| 1st time | Does the task. Saves a routine memory recording the operation and tier used. |
| 2nd time | Does the task. Mentions a tool or library that could handle it long-term. Updates the routine. |
| 3rd+ time | Suggests a script or dedicated CLI workflow. Explains the tradeoff. Updates the routine. |

### What counts as "the same operation"

The test: *"Could a single script handle both instances with just different input files?"*

**Same operation:**
- Extract text from one cheque photo, then another cheque photo (OCR on documents)
- Trim the intro off one podcast, then another podcast (audio trim)

**Not the same operation:**
- Generate a strategy deck, then a team intro deck (different content and structure — just both .pptx)
- Trim a podcast, then extract a clip from a video (related but different transformations)

Same output format does not mean same operation. Two slide decks with different content are two different tasks, not a repeated routine.

### Routine memory files

Routines are stored in the memory system as `routine_<slug>.md` files. Each records:
- What the operation is (verb + object)
- What input type it applies to
- A log of dates and tiers used
- What to suggest next time (the next escalation)

The user can browse, edit, or delete these files to steer Claude's behavior. Deleting a routine resets the count. Editing "Next escalation" changes what Claude suggests.

## Examples

| Task | Tier | Why |
|------|------|-----|
| Draft a project proposal | 0 | Content generation — model produces it directly |
| Trim 10s off a podcast | 1 | `ffmpeg -i input.mp3 -ss 10 output.mp3` |
| Grayscale a photo | 2 | Suggest imagemagick: `convert input.jpg -colorspace Gray output.jpg` |
| Extract text from a PDF | 1/2 | `pdftotext input.pdf output.txt` (poppler-utils, install if needed) |
| Analyze a 50-column CSV | 3 | Structured data — pandas script is the right tool |
| Caption a video | 3 | Multiple tools need orchestration (extract, transcribe, merge) |
| Extract text from cheque (3rd time) | 3 | Repeated routine — suggest an OCR script or CLI wrapper |

## Relationship to other patterns

This pattern is the *prerequisite* to the scripting patterns:

- **[pattern-scripts-from-prompting](pattern-scripts-from-prompting.md)** — describes the lifecycle *after* the decision to script is made (`.local/` → `scripts/src/` → tested CLI tool)
- **[pattern-cli-scripts](pattern-cli-scripts.md)** — describes *how* to build good scripts once you're building one (argparse, `--help`, `--dry-run`, tests)

Task escalation answers the question those patterns skip: "should I be writing a script at all?"
