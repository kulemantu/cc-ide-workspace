# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Layout

This is a Claude Code base project with three zones:

- **`workspace/`** — the user's space. Notes, documents, data files. Committed to git. Script outputs go to `workspace/outputs/`.
- **`scripts/`** — Python environment. Modules in `src/`, tests in `tests/`, managed by uv. See `scripts/CLAUDE.md` for commands.
- **`.local/`** — private operational context. Credentials, reference data, scratch work, one-off scripts. Gitignored.

## Key Rules

Detailed rules live in `.claude/rules/` and are loaded automatically. The essentials:

- **Git**: no auto-commit or auto-push. Propose the message and wait for approval. Conventional commits (`type(scope): description`), batched by concern.
- **Python**: always Python, never bash scripts. Always write tests. Run everything via `uv run` from `scripts/`.
- **Sessions**: maintain a session file in `.sessions/SESSION-YYYY-MM-DD-task-description.md`. Update it before context compaction.
- **Outputs**: all generated output — from scripts, analysis, or any Claude-generated content — goes to `workspace/outputs/`.
- **Workspace**: don't reorganize, rename, or move user files in `workspace/` without being asked.
- **Docs**: guides in `docs/` use `howto-*.md` and `pattern-*.md` naming. Update them when new patterns emerge from sessions.
