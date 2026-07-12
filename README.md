# cc-ide-workspace

An IDE-first workspace for [Claude Code](https://claude.ai/code). Open it in VS Code, JetBrains, or Cursor — and use the IDE as your primary app for all work, whether that's writing code, analyzing data, drafting documents, or managing projects.

## The Idea

Instead of switching between terminal, browser, file manager, and multiple apps — **work from one place**. The IDE gives you file browsing, an integrated terminal, MCP tools, and Claude Code side by side. Claude handles the technical plumbing (Python scripts, dependencies, testing) so you can focus on the work itself.

This workspace is structured so Claude knows where to put things, where to find your files, and how to maintain continuity across conversations.

## Quick Start

```bash
git clone https://github.com/kulemantu/cc-ide-workspace.git my-project
```

**Open `my-project/` in your IDE** — that's your starting point for everything. Claude manages the Python environment, dependencies, and tooling internally. You don't need to install or configure anything beyond Claude Code itself.

## Directory Structure

```
.
├── workspace/           # YOUR space — put your files here
│   ├── .outputs/        # Generated output — from scripts and Claude
│   └── CLAUDE.md        # Workspace rules for Claude
├── scripts/             # CLAUDE's space — Python code lives here
│   ├── src/             # Reusable modules Claude builds over time
│   ├── tests/           # Tests Claude writes for those modules
│   ├── pyproject.toml   # Dependencies and tool config
│   ├── uv.lock          # Dependency lock file
│   └── CLAUDE.md        # Python conventions for Claude
├── apps/                # SHAREABLE TOOLS — self-contained CLIs, one folder per app
├── docs/                # GUIDES — how-to and pattern docs for this workspace
├── .claude/rules/       # SHARED — behavior rules loaded automatically
├── .sessions/           # AUTO-MANAGED — Claude's session logs (gitignored)
├── .local/              # PRIVATE — credentials, scratch, sensitive data (gitignored)
├── CLAUDE.md            # Guidance for Claude
└── README.md            # This file
```

## Apps

Self-contained tools in `apps/` — each has its own README, tests, and CLI. Use them via Claude Code skills (type `/` to see available commands) or directly from the terminal.

| App | What it does | Requirements | Skill |
|-----|-------------|-------------|-------|
| [transcriber-prioritizer](apps/transcriber-prioritizer/) | Call recording → diarized transcript → structured notes | `uv`, `ffmpeg`, `OPENROUTER_API_KEY` | `/transcribe` |

### What each folder does

**`workspace/`** — This is yours. Drop files here: CSVs, PDFs, notes, documents, images, whatever you're working with. Claude reads from here when you ask it to process something. Generated output — from scripts, analysis, or any Claude-generated content — goes to `workspace/.outputs/`. Your files are version-controlled.

**`scripts/`** — Managed by Claude. When Claude needs to run code — analyze data, transform files, call APIs, generate reports — it writes Python scripts here. Over time, repeated operations get extracted into reusable modules in `scripts/src/`. Claude manages dependencies, writes tests, and keeps the code clean. You don't need to touch this folder.

**`apps/`** — Self-contained, shareable tools. Where `scripts/` is internal plumbing for *this* workspace, an app is something you could lift out and run elsewhere — one folder per app, each with its own entry point, tests, and `README.md`, and a self-documenting CLI (`--help`, `--json`). See `docs/pattern-apps.md`.

**`.sessions/`** — Auto-managed by Claude. Session files (`SESSION-YYYY-MM-DD-task-description.md`) capture what Claude was working on, what decisions were made, and what's next. Claude updates these before its conversation history is trimmed (context compaction) so nothing is lost between sessions. One file per task, not per day — so parallel worktrees don't collide.

**`.local/`** — Private and gitignored. Credentials, API keys, scratch data, reference documents, one-off scripts, working notes. Anything that shouldn't be committed but is useful for the project. Claude stores operational context here (prompts, runbooks, evidence).

**`.claude/rules/`** — Shared behavior rules that Claude loads automatically. These keep Claude consistent: commit style, Python conventions, session discipline. Rules are committed to the repo so your whole team gets the same Claude behavior.

### What Claude auto-manages

- **Session files** in `.sessions/` — created and updated automatically, capturing progress and decisions
- **Python environment** in `scripts/` — dependencies installed, code linted and type-checked, tests written
- **Output files** in `workspace/.outputs/` — generated from scripts, analysis, or any Claude-produced content

### Don't touch

- **`scripts/.venv/`** — Claude's virtual environment. Let Claude manage it.
- **`scripts/uv.lock`** — Dependency lock file. Claude keeps this in sync.
- **`.sessions/` files** — Claude maintains these for continuity. Editing them won't break anything, but Claude may overwrite your changes.

## Three-Layer Continuity

Claude doesn't start from zero each session. It reads three layers:

```
Layer 1: Code (git)       → what exists now
Layer 2: .sessions/       → why it was built, what was tried, what's next
Layer 3: .local/          → how to operate it (prompts, runbooks, credentials)
```

This means Claude picks up where it left off — it knows what was decided, what failed, what's pending, and what credentials or context are needed.

## Before a PR or external share

Run one local gate from the repository root:

```bash
uv run --project scripts python3 scripts/src/workspace_check.py verify
```

Raw screenshots, browser captures, exports, and client evidence belong in
`.local/` or the ignored capture paths. The gate blocks private-path and
high-confidence secret findings and flags media for manual review. See
[`docs/howto-share-safely.md`](docs/howto-share-safely.md) for the redaction and
audience checklist.

## Rules

Rules in `.claude/rules/` are loaded automatically. They enforce:

**Git conventions** — Conventional commits (`type(scope): description`). No auto-commit or auto-push — Claude proposes the message and waits for your approval. Commits batched by concern. `--force-with-lease` over `--force`.

**Python conventions** — Always Python, never bash scripts. Always write tests. Use ruff for linting, pyright for type checking, pytest for testing. All run via `uv`.

**Session discipline** — Claude saves progress to session files before its conversation history is trimmed. This means future sessions can resume without re-explaining context.

## Docs

The `docs/` directory contains guides for using this workspace across different scenarios. Naming convention:

- `howto-*.md` — task-oriented guides (MCP servers, worktrees, AI orchestration)
- `pattern-*.md` — reusable strategies (CLI scripts, the `apps/` folder type, scripts from prompting, .local directory usage)

These are opinionated patterns for how the workspace is designed to be used — not generic Claude Code documentation. Claude reads these for context when helping you with related tasks.

## MCP Integrations

MCP (Model Context Protocol) servers extend Claude beyond the filesystem. They work in both the IDE and the terminal.

### Recommended

| Server | What it enables |
|--------|----------------|
| **Context7** | Live documentation lookup for any library |
| **GitHub** | Create/review PRs, manage issues, search code |
| **Playwright** | Browser automation — navigate, click, screenshot, test |

### Worth adding for team workflows

| Server | What it enables |
|--------|----------------|
| **Jira** | Create/update tickets, link PRs to issues |
| **Slack** | Post deploy notifications, share PR links |
| **n8n** | Export/import workflows, trigger executions |

### How to set up MCPs

Start with **Context7**. Once you have it, you can ask Claude Code how to set up any other MCP server — Claude will look up the current docs and walk you through it. This applies to everything in this workspace: if you're unsure how something works, ask Claude.

For setup instructions, see the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) or ask Claude directly: *"How do I add the GitHub MCP server?"*

## Customizing

- **Rename the package**: update `name` in `scripts/pyproject.toml`
- **Add team rules**: create new `.md` files in `.claude/rules/`
- **Personal rules**: use `~/.claude/rules/` for rules that shouldn't be committed (e.g., your sign-off line)
- **Add dependencies**: Claude runs `uv add <package>` from `scripts/` as needed — or ask it to
