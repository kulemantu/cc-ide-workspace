# How-to — set up a frame-scoped workspace

## Purpose

Recipe for creating a new audience-scoped workspace under `workspace/`
following `docs/pattern-frame-scoped-workspace.md`. Use this when you need a
clean, DRY, crawl-ready workspace for a specific audience × scope.

## Before you start — confirm the pattern fits

Skip (use an ordinary sub-workspace instead) if any of these are true:

- The workspace will serve a single audience and a single framing → overkill.
- The work is short-term tactical (one-off report, single incident) → a
  leaf-doc, not a workspace.
- An existing workspace already covers the audience without framing conflicts.

Apply if:

- The same content must serve two distinct audiences with framing differences.
- An existing workspace has conflicting representations of shared entities (a
  person's role, a phase, a number).
- Synthesis quality is degrading — the wrong context is leaking into artefacts.

## Steps

### 1. Decide the frame

Write down (in `.scratchpads/<frame>-frame-draft.md`):

- **Frame name** — short, kebab-cased (e.g. `q3-leadership-update`).
- **Audience** — names + roles of the people who will read the artefacts.
- **Subject scope** — what's in scope.
- **What this is NOT** — the adjacent frames it must not be confused with.
- **Adjacent workspaces** — existing workspaces this one will reference.

This becomes the boilerplate for the frame statement at the top of every file.

### 2. Create the folder skeleton

```bash
mkdir -p \
  workspace/<frame>/.context \
  workspace/<frame>/.source \
  workspace/<frame>/draft \
  workspace/<frame>/.scratchpads \
  workspace/<frame>/.outputs
```

`.scratchpads/` is gitignored (see the repo `.gitignore`); the others tracked.

### 3. Write `CLAUDE.md` and `README.md`

- `CLAUDE.md` — frame statement + folder structure + crawl order +
  cross-workspace whitelist/blacklist + frame-shift signals + render rule.
- `README.md` — human-friendly overview: what the workspace is, the latest
  output, how to navigate, who to ask.

### 4. Curate `.context/`

Required files:

- `index.md` — short crawl entrypoint; lists the other files.
- `frame.md` — audience, scope, "what this is NOT".
- `people.md` — translation table: per-frame role mapping for shared entities.
  One row per person who appears in this frame and at least one other; a column
  for each frame.
- `timeline.md` — frame-native phasing + translation table to neighbouring
  frames' phasing.
- `references.md` — explicit whitelist of cross-workspace paths with frame-shift
  notes (Path / Use for this frame / Do NOT pull).

Add a metric-anchor file (`unit-economics.md` or equivalent) if the frame has a
quantitative spine.

Each file leads with the frame statement: *"Frame: \<name\>. Audience:
\<audience\>. What this is NOT: \<adjacent frame\>."*

### 5. Identify upstream sources for `.source/`

For each upstream canonical file you will be enhancing, check:

- Is it canonical for this frame?
- Did it come from upstream (a collaborator / external system)?
- Will you *enhance* it (extract numbers, build narrative, render derivatives)
  rather than edit it in place?
- Is it sensitive? — No → `.source/`. Yes → `.scratchpads/` instead.

Move each into `.source/` (or `.scratchpads/` if sensitive). Add an entry to
`.source/README.md` per file: Origin / Used by.

### 6. Decide cross-workspace handling

For every file in another workspace this frame might need, apply the
move / copy / reference decision tree in
`docs/pattern-frame-scoped-workspace.md`. **Never copy a canonical file** — the
drift cost is silent. Use a reference + a frame-shift note.

### 7. Write `draft/` narratives

Create the canonical markdown for this frame. Each leads with the frame
statement. Use sequenced filenames (`01-…`, `02-…`) when there's a defined
render order. Diagram source (`.d2` / `.mmd`) goes in `draft/diagrams/`; renders
are derived.

### 8. Render artefacts to `.outputs/`

Produce the rendered deliverables from the canonical markdown. Re-render before
sharing externally.

### 9. Verify

Walk through the "Drift-prevention mechanisms" in
`docs/pattern-frame-scoped-workspace.md` and confirm each is in place:

- Frame statement at the top of every `.context/`, `.source/`, `draft/` file.
- Translation tables in `.context/people.md` and `.context/timeline.md`.
- `CLAUDE.md` whitelist + blacklist and human pause-points.

Drift test: ask Claude "What is \<shared entity\>'s role in this frame?" and
confirm the answer matches `.context/people.md`, not the other-frame view.

Crawl test: ask Claude to generate a one-pager for this frame's audience.
Confirm it crawls only this workspace, not adjacent ones.

## Maintenance

- When you add a new shared entity, add it to `.context/people.md`.
- When a phase boundary changes, update `.context/timeline.md`.
- When you cross a workspace boundary for the first time, add the path to
  `.context/references.md` (after the human OKs it).
- When a `draft/` file changes, the corresponding `.outputs/` artefact is stale
  — re-render before sharing.

## Related

- `docs/pattern-frame-scoped-workspace.md` — the pattern this how-to instantiates.
- `docs/howto-workspace-conventions.md` — repo-wide workspace zone + naming conventions.
