# workspace/

This is the user's space — notes, documents, data files, and any other files
the user is working with.

## Sub-workspace model

`workspace/` holds **one folder per workstream** (a project, deliverable, or
research thread) — not a flat pile of files. Each sub-workspace owns its zones:
outputs and scratchpads are **per-subfolder**, not a single top-level drawer.

```
workspace/
├── example-workstream/   # worked example — copy this shape, then rename/delete
│   ├── .source/          # read-only canonical inputs (tracked)
│   ├── draft/            # your canonical markdown (tracked)
│   ├── .scratchpads/     # working drafts (gitignored, created on demand)
│   ├── .outputs/         # generated artefacts (tracked)
│   └── CLAUDE.md         # folder purpose
└── CLAUDE.md             # this file
```

See `workspace/example-workstream/CLAUDE.md` for what each zone is for, and
`docs/howto-workspace-conventions.md` for the full reference.

## Filename naming

| Pattern | When |
|---|---|
| `YYYY-MM-DD-description.md` | Time-series — many files of the same type in one folder (check-ins, daily logs) |
| `description-YYYY-MM-DD.md` | Mixed outputs — few files of different types; the date qualifies the artefact |
| `descriptive-name-template.md` | Templates and reference docs |
| `NN-descriptive-name.md` | Sequenced files with a defined reading / rollout order |

Default to **no version in the filename** — git is the version history. Use a
`-vN` suffix only when multiple shipped versions of a recipient-facing artefact
must coexist; highest N is current.

## Dot-prefix folders

| Prefix | Meaning | Committed? |
|---|---|---|
| `.outputs/` | Generated artefacts — the "published" drawer | ✔ tracked |
| `.scratchpads/` | Intermediate working drafts; sensitive sources | ✘ gitignored |
| `.source/` | Read-only canonical upstream inputs being enhanced | ✔ tracked |
| `.context/` | Curated, frame-tagged crawl entrypoint (frame-scoped workspaces only — see `docs/pattern-frame-scoped-workspace.md`) | ✔ tracked |
| `.local-files/` | Private / sensitive material inside `workspace/` | ✘ gitignored |

## Rules

- Don't create scripts or code files here — those belong in `scripts/`.
- Don't reorganize, rename, or move the user's files without being asked.
- Generated output goes to `workspace/<subfolder>/.outputs/`, scoped to its
  workstream — not a single shared top-level folder.
- Input files the user places here can be read by scripts in `scripts/`.
- Don't commit `.scratchpads/` or `.local-files/`; check for credentials before
  referencing them in conversation output.
