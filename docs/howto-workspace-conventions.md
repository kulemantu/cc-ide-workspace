# How-to — Workspace Conventions

## Purpose

Reference for how content is organised in `workspace/` — so new collaborators
(and future-you) can find things and put new files in the right place.

## Sub-workspace model

`workspace/` holds **one folder per workstream** — a project, a deliverable, a
research thread. Each sub-workspace owns its own zones; outputs and scratchpads
are per-subfolder, not a single shared top-level drawer. `workspace/example-workstream/`
is a worked example of the shape — copy it, then rename or delete it.

## Zones

| Zone | What's there | Committed? |
|---|---|---|
| `workspace/<subfolder>/` | A workstream — user-owned content and deliverables | ✔ |
| `workspace/<subfolder>/.source/` | Read-only canonical upstream inputs being enhanced | ✔ |
| `workspace/<subfolder>/draft/` | Your own canonical markdown narratives (precedes `.outputs/`) | ✔ |
| `workspace/<subfolder>/.scratchpads/` | Intermediate working drafts; sensitive sources | ✘ gitignored |
| `workspace/<subfolder>/.outputs/` | Script output, analysis, generated content | ✔ |
| `workspace/<frame-scoped>/.context/` | Curated, frame-tagged crawl entrypoint (frame-scoped workspaces only — see `pattern-frame-scoped-workspace.md`) | ✔ |
| `workspace/.local-files/` | Private / sensitive material (contracts, credentials, working notes) | ✘ gitignored |
| `.local/` | Operational context: credentials, scratch, reference data | ✘ gitignored |
| `.sessions/` | Per-task session logs for continuity across conversations | ✘ gitignored |

## Naming

| Pattern | When |
|---|---|
| `YYYY-MM-DD-description.md` | Time-series — many files of the same type in one folder (check-ins, daily logs) |
| `description-YYYY-MM-DD.md` | Mixed outputs — few files, different types; the date qualifies the artefact |
| `descriptive-name-template.md` | Templates and reference docs |
| `NN-descriptive-name.md` | Sequenced files with a defined reading / rollout order |

### Versioning

- **Default:** no version in the filename — git is the version history.
- **Point-in-time records** (check-ins, reports): date in filename; never
  modify after creation.
- **External deliverables** (artefacts shared outside the team): a `-vN` suffix
  only when multiple versions must coexist for recipients. Highest N is current;
  never keep both an unsuffixed and a versioned file for the same artefact.

## Dot-prefix folder conventions

| Prefix | Meaning |
|---|---|
| `.outputs/` | Generated artefacts — **tracked in git** |
| `.scratchpads/` | Intermediate working docs; sensitive sources — **gitignored** |
| `.source/` | Read-only canonical upstream inputs being enhanced — **tracked** |
| `.context/` | Curated, frame-tagged crawl entrypoint — **tracked** (frame-scoped workspaces) |
| `.local-files/` | Private material inside `workspace/` — **gitignored** |
| `.<name>-wip/` | Near-final deliverables, not yet ready to share externally — tracked *eventually*; rename to `<name>/` (no dot) when ready |

The `.outputs/` vs `.scratchpads/` split gives each workstream both a committed
"published" drawer and an ignored "working" drawer, without cluttering the repo
with build artefacts.

`.source/` vs `.scratchpads/`: both can hold inputs. Use `.source/` for inputs
that are canonical *and* safe to commit. Use `.scratchpads/` when the input is
sensitive (credentials, honest assessments, draft positioning) or still
evolving. `.source/` is distinct from `draft/` — `.source/` is what you
received; `draft/` is what you author.

## Source-of-truth rules

- **Markdown is canonical for text deliverables.** Rendered `.docx` / `.pptx` /
  `.html` are one-off outputs — they drift from source fast. When the binary
  disagrees with the markdown, the markdown wins; re-render before sharing.
- **Diagram source is canonical, not the render.** Edit the `.mmd` / `.d2`
  source first, regenerate `.svg` / `.png` after.
- **Files received from others keep their original filename** — don't rename
  them to fit conventions; that loses provenance. Put them in `.source/`.

## Bootstrapping a new workstream folder

1. `mkdir -p workspace/<workstream>/{.source,draft,.outputs}` — tracked zones.
2. Add a `CLAUDE.md` inside describing the folder's purpose and structure.
3. `.scratchpads/` is created on demand — it's gitignored, no need to commit it.
4. Add the first working file using the naming convention above.

## Related

- `workspace/CLAUDE.md` — the authoritative naming convention reference.
- `workspace/example-workstream/` — a worked example of the sub-workspace shape.
- `docs/pattern-frame-scoped-workspace.md` — when to split a workspace for a
  specific audience × scope; documents the `.context/` zone.
- `docs/howto-set-up-frame-scoped-workspace.md` — recipe for the frame-scoped variant.
- `.claude/rules/sessions.md` — session file lifecycle and three-layer continuity.
