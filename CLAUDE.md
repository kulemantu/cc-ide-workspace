# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Layout

This is a Claude Code base project with these zones:

- **`workspace/`** — the user's space. Notes, documents, data files. Committed to git. Script outputs go to `workspace/.outputs/`.
- **`scripts/`** — Python environment. Modules in `src/`, tests in `tests/`, managed by uv (Python 3.12+). See `scripts/CLAUDE.md` for conventions.
- **`apps/`** — self-contained, shareable tools/CLIs (one folder per app: entry point + tests + README). Lift-out-and-run-elsewhere, vs. `scripts/` which is internal plumbing. Apps invoke via `uv run python3` like everything else, but may be stdlib-only + `unittest` (skipping ruff/pyright) for portability — documented per app. See `docs/pattern-apps.md`.
- **`.claude/skills/`** — user-facing skills wrapping app CLIs (e.g. `/transcribe` wraps `apps/transcriber-prioritizer`). Skill name = action verb, not the app directory name. A skill is a thin wrapper: check prerequisites, guide setup if missing, call the app's CLI — never duplicate its logic.
- **`.local/`** — private operational context. Credentials, reference data, scratch work, one-off scripts. Gitignored.

Code graduates outward: `.local/` (scratch) → `scripts/src/` (reusable) → `apps/<name>/` (shareable: own README, tests, self-documenting CLI with `--help`/`--json`).

## Commands

All Python commands run from `scripts/`:

```bash
cd scripts
uv run pytest                              # Run all tests
uv run pytest tests/test_foo.py::test_bar  # Run a single test
uv run ruff check .                        # Lint
uv run ruff format .                       # Format
uv run pyright                             # Type check
uv run python src/my_script.py             # Run a script
uv sync                                    # Sync deps when .venv is missing or deps change
uv add <package>                           # Add a dependency
```

Apps run from the repo root and test with stdlib unittest:

```bash
uv run python3 apps/transcriber-prioritizer/transcribe_call.py --help
cd apps/transcriber-prioritizer && uv run python3 -m unittest test_transcribe_call -v
```

Never use bare `python` — always `uv run` so commands use the managed environment.

## Key Rules

Detailed rules live in `.claude/rules/` and are loaded automatically. The essentials:

- **Git**: no auto-commit or auto-push. Propose the message and wait for approval. Conventional commits (`type(scope): description`), batched by concern.
- **Python**: always Python, never bash scripts. Always write tests. Run everything via `uv run` — from `scripts/` for the managed environment, or from the app directory for apps.
- **Sessions**: maintain a session file in `.sessions/SESSION-YYYY-MM-DD-task-description.md`. Update it before context compaction.
- **Outputs**: all generated output — from scripts, analysis, or any Claude-generated content — goes to `workspace/.outputs/`.
- **Workspace**: don't reorganize, rename, or move user files in `workspace/` without being asked.
- **Docs**: guides in `docs/` use `howto-*.md` and `pattern-*.md` naming. Update them when new patterns emerge from sessions.
