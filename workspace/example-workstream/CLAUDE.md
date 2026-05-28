# example-workstream/

A worked example of a **sub-workspace** — one folder per workstream (a project,
a deliverable, a research thread). Copy this shape for real work; rename or
delete this folder once you start.

## Why sub-workspaces

`workspace/` holds one folder per workstream rather than a flat pile of files.
Each workstream gets its own zones, so generated artefacts and working drafts
stay scoped to the work they belong to instead of one shared top-level drawer.

## Zones

| Zone | What goes here | Committed? |
|---|---|---|
| `.source/` | Read-only canonical inputs from upstream — files you received and will *enhance*, not edit in place. Provenance stays intact. | ✔ tracked |
| `draft/` | Your own canonical markdown — the narratives/content you author. Renderers and outputs derive from here. | ✔ tracked |
| `.scratchpads/` | Working drafts, intermediate exploration, sensitive sources. No editing discipline. Created on demand — gitignored, so it won't exist until you `mkdir` it. | ✘ gitignored |
| `.outputs/` | Generated artefacts — script output, rendered documents, analysis. The "published" drawer. | ✔ tracked |

`.source/` vs `.scratchpads/`: both can hold inputs. Use `.source/` for inputs
safe to commit; use `.scratchpads/` when the input is sensitive (credentials,
honest assessments, draft positioning) or still churning.

## Rules

- Don't create scripts or code files here — those belong in `scripts/`.
- Don't reorganize, rename, or move the user's files without being asked.
- Markdown in `draft/` is canonical; rendered binaries in `.outputs/` drift —
  re-render from source before sharing.

## Bootstrapping a new workstream folder

1. `mkdir -p workspace/<name>/{.source,draft,.outputs}` — tracked zones.
2. Add a `CLAUDE.md` describing the folder's purpose (this file is the model).
3. `.scratchpads/` is created on demand; it's gitignored, no need to commit it.
4. Add the first file using the naming conventions in `workspace/CLAUDE.md`.

See `docs/howto-workspace-conventions.md` for the full zone + naming reference,
and `docs/pattern-frame-scoped-workspace.md` for the heavier audience-scoped
variant that adds a `.context/` zone.
