# Pattern: `apps/` — shareable working tools

`apps/` is a folder type for **self-contained, shareable working tools / CLIs**,
sitting alongside `scripts/`. Where `scripts/` is internal plumbing Claude
accretes for *this* workspace, an app is something you could lift out and run
elsewhere as-is.

## `apps/` vs `scripts/`

| | `scripts/` | `apps/` |
|---|---|---|
| **What** | A collection of Python scripts + reusable `src/` modules Claude accretes | Self-contained, **shareable working tools / CLIs** |
| **Boundary** | Internal to this workspace | Could be lifted out and run elsewhere as-is |
| **Shape** | `src/` modules + tests, one shared `pyproject.toml` | One folder per app: entry point + tests + README, own deps story |
| **Interface** | Called by Claude during tasks | Self-documenting CLI (`--help`, subcommands, `--json`) |
| **Example** | a workspace-specific sync/report script | `transcriber-prioritizer/` (media → transcript → notes, runs anywhere) |

Rule of thumb: if you'd send it to a colleague to run on their machine, it's an
**app**. If it only makes sense inside this workspace, it's a **script**.

## App conventions

- One directory per app: `apps/<name>/`.
- Self-documenting CLI: `--help` lists all capabilities; `--json` for machine
  output (see `docs/pattern-cli-scripts.md` for the CLI conventions).
- Tests live beside the app (`test_*.py`).
- A `README.md` with usage + roadmap.
- If the app needs secrets/config, ship a committed `.env.example` template; the
  real `.env` is gitignored. Read keys from the environment, never from argv.

## Tooling carve-out

The workspace default (`.claude/rules/python-tooling.md`) is `uv` / `ruff` /
`pyright`, run from `scripts/`. Apps always use `uv run python3` as their
invocation — both inside this workspace and externally — since `uv` is a single
binary that installs in one command. Some apps are deliberately **stdlib-only +
`unittest`** for zero-install portability — e.g. `transcriber-prioritizer`, so it
runs on any box with `python3` + `uv` + `ffmpeg` with no `pip install` step. This
is an intentional, documented divergence from `ruff`/`pyright`, not drift: state it
in the app's README, and keep such apps free of `pip install` requirements.

## When scripts graduate to apps

A script in `scripts/src/` is a candidate for `apps/` when:

1. It's **self-contained** — doesn't import other `scripts/src/` modules
2. It's **general** — useful outside this workspace (you'd send it to a colleague)
3. It has a **CLI interface** — `--help`, subcommands, `--json` output
4. It has **tests** alongside it

The graduation path: `.local/` (scratch) -> `scripts/src/` (reusable) ->
`apps/<name>/` (shareable). Moving to `apps/` means giving it its own directory,
README, and dependency story.

## Making apps discoverable

Apps with a CLI can expose **Claude Code skills** in `.claude/skills/` so
collaborators find them via `/` autocomplete without reading docs.

The discovery path:

1. **`README.md`** lists all apps in a table (name, one-liner, requirements, skill)
2. **`apps/<name>/README.md`** documents available skills and common options
3. **`.claude/skills/<action>.md`** is a thin wrapper: check prerequisites, guide
   setup if missing, run the CLI, report results

Conventions:

- Skill name = the user-facing **action verb** (`transcribe`), not the directory
  name (`transcriber-prioritizer`). One skill per user-facing action.
- The skill handles onboarding: if prerequisites (API keys, system deps) are
  missing, it guides the user through setup instead of failing.
- The app's CLI is the engine; the skill is the TUI integration layer. Don't
  duplicate logic — the skill calls the CLI.
