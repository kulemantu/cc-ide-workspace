# Changelog

Reverse-chronological log of significant changes to this workspace — decisions,
new artefacts, retired content, sources ingested. Trivial commits don't need an
entry; significant moments do. Git holds the full history; this file is the
human-readable highlight reel.

**Entry format** — newest first:

```
## YYYY-MM-DD — short title

**Decisions** — what was decided and why
**New** — artefacts/workstreams added
**Retired** — what was removed or superseded
**Open / next** — what's still in flight
```

Not every sub-section is needed in every entry — keep only the ones that apply.

---

## 2026-06-18 — apps/ folder type + transcriber-prioritizer

**Decisions** — Introduce `apps/` as a folder type for self-contained, shareable
tools, distinct from `scripts/` (internal workspace plumbing). Apps may diverge
from the `uv`/`ruff`/`pyright` default when portability warrants it, documented
per app.

**New**
- `apps/transcriber-prioritizer/` — stdlib-only Python + `ffmpeg` CLI: a call
  recording → speaker-labelled transcript → structured, prioritized notes via
  OpenRouter. Ships `.env.example`; key read from `OPENROUTER_API_KEY` env only.
- `docs/pattern-apps.md` — the `apps/` vs `scripts/` convention and the
  stdlib-only tooling carve-out.
- `.gitignore` — guards `.env` (keeps `*.env.example`) and generated
  media/outputs (`*.mp3`, `*.transcript.md`, `*.notes.md`).
