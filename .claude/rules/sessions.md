# Session Files

All session data lives under gitignored directories — never in the repo root.

- `.sessions/` — session logs named `SESSION-YYYY-MM-DD-task-description.md` (one per task, not per day — multiple worktrees can run in parallel)
- `.local/` — operational context (gitignored):
  - Credentials & secrets
  - Analysis & planning docs
  - Reference data (PDFs, JSON exports, screenshots)
  - One-off scratch scripts
  - AI prompts and working notes

## Rules
- Never commit contents of `.sessions/` or `.local/`
- Check for credentials before referencing session contents in conversation output
- Never delete session files — minify instead
- Translate valuable content to permanent docs in `docs/`
- Update with context, session logs, and learnings during work
- **Before context compaction**: always update the session file with current progress, pending work, and any decisions or context that would be lost. The session file is the recovery point after compaction — treat it as the handoff to your future self.

## Session File Template

```markdown
# Session — YYYY-MM-DD — task-description

## Task
What you're working on.

## Context
Background, constraints, prior state.

## Changes
- What was done (bullet list)

## Key Decisions
- Decisions made and why

## Credentials
(if any — never commit)
```

## Session Lifecycle
1. **Capture** — detailed notes, code snippets, investigation steps, credentials
2. **Review** — check for sensitive information
3. **Translate** — move useful content to permanent docs
4. **Update Rules** — if new patterns discovered
5. **Minify** — reduce to essential format: Task/Outcome/Changes/Docs Updated/Key Decisions/Credentials

## Three-Layer Continuity Model

```
Layer 1: Code (git)         → what exists now
Layer 2: .sessions/         → why it was built, what was tried, what's next
Layer 3: .local/            → how to operate it (prompts, runbooks, credentials, evidence)
```

Claude reads all three layers to build a complete picture. A new session starts from the code, plus the narrative of how it got there, plus the operational context for working with it.
