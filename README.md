# Claude Code Base Project

A ready-to-go project template for working with [Claude Code](https://claude.ai/code). Works for both coding and non-coding tasks — drop in your files, and Claude has a structured workspace with Python available when scripting is the right tool for the job.

## Why This Exists

Claude Code runs in a terminal with access to your filesystem. A bare directory works, but you lose out on:

- **Shared rules** that keep Claude consistent across your team (commit style, tooling, session tracking)
- **A Python environment** so Claude can write and run scripts directly (`uv run python script.py`) instead of cramming logic into `python -c` one-liners in bash
- **Session files** that survive context compaction — Claude's memory of what it was doing persists locally even when conversation history is trimmed
- **Guardrails** like no auto-commit, conventional commits, and structured session logs that make AI-assisted work reviewable

## Quick Start

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.12+

### Setup
```bash
git clone <this-repo> my-project
cd my-project
uv sync
```

That's it. Claude Code will pick up the rules from `.claude/rules/` and `CLAUDE.md` automatically.

## How to Use

### For coding tasks
Write application code in `src/new_project/`, tests in `tests/`. The full Python toolchain is configured — ruff, pyright, pytest — all runnable via `uv run`.

### For non-coding tasks
Drop files (CSVs, PDFs, logs, data) anywhere in the project. When Claude needs to process them, it can write a Python script and run it with `uv run python script.py` rather than fighting with bash one-liners or `python -c`. This matters because:

- Scripts are readable, editable, and rerunnable
- Dependencies can be added to `pyproject.toml` and installed with `uv sync`
- Complex logic (data transforms, API calls, file processing) belongs in `.py` files, not shell commands

### For mixed tasks
Most real work is mixed. You might ask Claude to analyze a CSV, then build a small tool around the analysis. The project structure supports both without switching setups.

## Project Structure

```
.
├── .claude/rules/       # Shared rules (committed, auto-loaded by Claude Code)
│   ├── git-conventions.md   # Commit style, no auto-push
│   ├── python-tooling.md    # uv, ruff, pyright
│   └── sessions.md          # Session file workflow
├── .sessions/           # Per-task session logs (gitignored)
├── .local/              # Credentials & scratch data (gitignored)
├── src/new_project/     # Application source
├── tests/               # Test suite
├── CLAUDE.md            # Quick-reference for Claude Code
└── pyproject.toml       # Python config (deps, ruff, pyright, pytest)
```

## Rules

Rules in `.claude/rules/` are loaded automatically by Claude Code. They enforce:

**Git conventions** — conventional commits (`type(scope): description`), no auto-commit or auto-push, batch commits by concern, `--force-with-lease` over `--force`.

**Python tooling** — always `uv run` (never bare `python`), ruff for linting/formatting, pyright for type checking.

**Session tracking** — session files in `.sessions/SESSION-YYYY-MM-DD-task-description.md` capture progress, decisions, and context. One file per task, not per day, so parallel worktrees don't collide. Claude updates the session file before context compaction so nothing is lost.

## Session Workflow

Session files are gitignored scratch — they exist for continuity, not for review. The lifecycle:

1. **Capture** — Claude writes detailed notes during work
2. **Review** — check for sensitive information before sharing
3. **Translate** — move useful content to permanent docs in `docs/`
4. **Update Rules** — if new patterns are discovered
5. **Minify** — reduce to essentials once the task is done

## Customizing

- **Rename the package**: update `name` in `pyproject.toml`, rename `src/new_project/`, and update `[tool.hatch.build.targets.wheel]`
- **Add dependencies**: `uv add <package>`
- **Add team rules**: create new `.md` files in `.claude/rules/`
- **Personal overrides**: use `~/.claude/rules/` for rules that shouldn't be committed (e.g., your sign-off line)
