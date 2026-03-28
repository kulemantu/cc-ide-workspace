# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                        # Install dependencies
uv run pytest                  # Run all tests
uv run pytest tests/test_foo.py::test_bar  # Run a single test
uv run ruff check .            # Lint
uv run ruff format .           # Format
uv run pyright                 # Type check
uv run python -m new_project   # Run the app
```

Always use `uv run` — never bare `python` or `python -m`.

## Architecture

- **src layout**: application code lives in `src/new_project/`, tests in `tests/`
- **Build backend**: hatchling
- **Python**: 3.12+

## Key Rules

Detailed rules live in `.claude/rules/` and are loaded automatically. The essentials:

- **Git**: no auto-commit or auto-push — propose the message and wait for approval. Conventional commits (`type(scope): description`), batched by concern.
- **Sessions**: maintain a session file in `.sessions/SESSION-YYYY-MM-DD-task-description.md`. Update it before context compaction — it's the recovery point.
- **Tooling**: ruff for lint/format, pyright for types, pytest for tests — all via `uv run`.
