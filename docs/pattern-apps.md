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
`pyright`, run from `scripts/`. Some apps are deliberately **stdlib-only +
`unittest`** for zero-install portability — e.g. `transcriber-prioritizer`, so it
runs on any box with `python3` + `ffmpeg`. This is an intentional, documented
divergence, not drift: state it in the app's README, and keep such apps free of
`pip install` requirements.
