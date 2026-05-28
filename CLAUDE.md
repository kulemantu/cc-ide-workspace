# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Layout

An IDE-first workspace where Claude Code handles technical plumbing (Python scripts, dependencies, testing) while the user focuses on their work. Three zones:

- **`workspace/`** — the user's space. Notes, documents, data files. Committed to git. Organised as **one sub-folder per workstream** (`workspace/<subfolder>/`); each sub-folder owns its own `.source/`, `draft/`, `.scratchpads/`, `.outputs/`. See `workspace/CLAUDE.md` and `docs/howto-workspace-conventions.md`.
- **`scripts/`** — Python environment. Modules in `src/`, tests in `tests/`, managed by uv (Python 3.12+). See `scripts/CLAUDE.md` for conventions.
- **`.local/`** — private operational context. Credentials, reference data, scratch work, one-off scripts. Gitignored.

Root-level trackers — `TODO.md` (day-level checklist), `CHANGELOG.md` (significant changes), `MAINTAINERS.md` (operational guide).

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

Never use bare `python` — always `uv run`. This is enforced by a hook that blocks bare `python`/`python3` commands.

## Key Rules

Detailed rules live in `.claude/rules/` and are loaded automatically. The essentials:

- **Scripting is a last resort.** Do the work directly from model context (Tier 0) or with a CLI tool via Bash (Tier 1-2) before reaching for a Python script (Tier 3). Ask the user before writing scripts. See `.claude/rules/scripting-philosophy.md` for the full escalation ladder.
- **Git**: no auto-commit or auto-push. Propose the message and wait for approval. Conventional commits (`type(scope): description`), batched by concern.
- **Python** (when scripting is justified): always Python, not bash scripts. Always write tests. Run everything via `uv run` from `scripts/`.
- **Sessions**: maintain a session file in `.sessions/SESSION-YYYY-MM-DD-task-description.md`. Update it before context compaction.
- **Outputs**: generated output goes to `workspace/<subfolder>/.outputs/` — scoped to its workstream, not a single top-level drawer.
- **Workspace**: don't reorganize, rename, or move user files in `workspace/` without being asked.
- **Docs**: guides in `docs/` use `howto-*`, `pattern-*`, `initiative-*`, `deliverable-*`, `reference-*` naming (see `.claude/rules/docs.md`). Update them when new patterns emerge from sessions.

## Hooks

Hooks in `.claude/hooks/` enforce rules automatically via `.claude/settings.json`. Key behavioral impacts:

- **Bare python blocked** — `python foo.py` is rejected; must use `uv run python foo.py`
- **Workspace/sessions/local protected** — `rm` on `workspace/`, `.sessions/`, `.local/` is blocked
- **Commit format validated** — commits must match `type(scope): description`
- **Push requires approval** — `git push` triggers interactive confirmation
- **Auto-format on save** — Python files are auto-formatted with `ruff format` after Edit/Write
- **Session reminder on compaction** — PreCompact hook reminds to update `.sessions/` before context is trimmed
- **Startup context injection** — SessionStart hook injects three-layer continuity context

See `docs/howto-hooks.md` for testing hooks, adding new ones, and disabling them.
