# Maintainers Guide

Operational guide for current and future maintainers of this repo. Complements
`README.md` — the README explains *what this workspace is*; this file is for the
person who needs to *do something* (run the tooling, add a workstream, hand the
repo off).

> Template stub — fill in the maintainers block and trim the workflows to match
> the real work once this workspace is in use.

## Current maintainers

- **Your name** — workspace owner · _contact_

Add a row per maintainer as the team grows: name · role · contact.

## Repo layout (quick map)

```
.
├── workspace/        # the work — one sub-folder per workstream
│   └── <workstream>/ # .source/ · draft/ · .scratchpads/ · .outputs/ + CLAUDE.md
├── docs/             # patterns · how-tos · initiative summaries · deliverables
├── scripts/          # Python utilities (managed by uv)
├── .local/           # gitignored — credentials + private operational context
├── .sessions/        # gitignored — per-task session logs
├── README.md         # what this workspace is + navigation
├── MAINTAINERS.md    # this file
├── TODO.md           # day-level tracker
└── CHANGELOG.md      # reverse-chronological change log
```

## Local setup

```bash
cd scripts
uv sync                # install the Python env (uv-managed, Python 3.12+)
uv run pytest          # verify — full test suite
uv run ruff check .    # verify — lint
```

## Common workflows

### Add a new workstream folder

See "Bootstrapping a new workstream folder" in
`docs/howto-workspace-conventions.md`. In short: `mkdir` the tracked zones, add
a `CLAUDE.md`, start the first file.

### Add an entry to the changelog

Open `CHANGELOG.md` and prepend a new `## YYYY-MM-DD — title` block at the top
(after the intro). Trivial commits don't need an entry; significant moments do.

## Where things live

| Need to find | Path |
|---|---|
| Canonical content for a workstream | `workspace/<workstream>/draft/` |
| Generated / rendered artefacts | `workspace/<workstream>/.outputs/` |
| Read-only upstream inputs | `workspace/<workstream>/.source/` |
| Patterns + how-tos | `docs/pattern-*.md` · `docs/howto-*.md` |
| Python utilities | `scripts/src/` |
| Per-task session logs | `.sessions/SESSION-YYYY-MM-DD-*.md` (gitignored) |
| Credentials / private context | `.local/` and `workspace/.local-files/` (gitignored) |

## Common gotchas

1. **Markdown is canonical; rendered binaries drift.** Always re-render before
   sharing externally.
2. **Scripts belong in `scripts/`, not `workspace/`.** `workspace/CLAUDE.md`
   enforces this.
3. **Never use bare `python`.** Use `uv run` from `scripts/` — a hook blocks
   bare `python`/`python3`.
4. **Don't auto-commit.** Confirm changes with the user before staging. See
   `.claude/rules/git-conventions.md`.

## Handoff

When handing this repo to the next maintainer:

1. Walk them through `README.md` (context) and this file (operational mechanics).
2. Confirm `cd scripts && uv sync && uv run pytest` passes on their machine.
3. Hand over `.local/` and `workspace/.local-files/` access (credentials)
   separately — those are gitignored and not in this repo.
4. Add their name to the "Current maintainers" block above.
