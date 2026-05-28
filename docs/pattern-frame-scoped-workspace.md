# Pattern — frame-scoped workspace

## What it is

A folder shape for splitting a workspace by **audience × scope frame** so that
artefact synthesis stays clean — no context leakage from neighbouring frames,
no drift on shared entities, no re-derivation of context that's already
curated.

This is the heavier, opt-in variant of the ordinary sub-workspace
(`docs/howto-workspace-conventions.md`). It adds a `.context/` zone and a
cross-frame translation discipline on top of the usual
`.source/ · draft/ · .scratchpads/ · .outputs/` zones.

The ordinary sub-workspace breaks down once a single workspace has to serve
**more than one audience**. The same entity — a person, a date, a number — gets
framed differently per audience, and when you generate an artefact for audience
A, the framing for audience B bleeds in. The frame-scoped pattern resolves this
by giving each frame its own folder with a 5-zone shape and an explicit
cross-frame translation layer.

**Example.** One project workspace produces both a *leadership update* and a
*team update* from the same material. The leadership update calls a milestone
"the Q3 launch commitment"; the team update calls the same milestone "the
redesign work" — one milestone, two framings. A contributor who is "a new
senior hire" in the leadership frame is "the lead on the redesign" in the team
frame. Draft the leadership update without isolating its context and the
team-frame phrasing leaks straight in. Give each audience its own frame folder,
plus a translation table for the shared milestone and contributor, and it
doesn't.

## Why

Three failures the pattern prevents:

1. **Context leakage** — full-context files (org charts, mixed budgets) bleed
   into single-purpose artefacts. The pattern isolates each frame's curated
   context in `.context/`.
2. **Drift on shared entities** — the same person/term/phase has different
   framings per audience. The pattern requires explicit translation tables in
   `.context/people.md` and `.context/timeline.md`.
3. **Re-derivation cost** — every new artefact re-asks "who is X / what's the
   timeline / what's the key metric" because the answer wasn't curated. The
   pattern caches the answer once in `.context/`, so synthesis is DRY.

Headline test: a new contributor (or new Claude session) can open the
workspace, read `.context/index.md`, and be productive without crawling other
workspaces. If they can't, the pattern is failing.

## The 5-zone shape

```
workspace/<frame-name>/
├── CLAUDE.md             # frame statement + crawl rules + whitelist/blacklist
├── README.md             # human overview + index links
├── .context/             # curated, frame-filtered, frame-tagged (tracked)
├── .source/              # read-only canonical upstream inputs (tracked)
├── draft/                # your canonical markdown narratives (tracked)
├── .scratchpads/          # working drafts; sensitive sources (gitignored)
└── .outputs/             # rendered artefacts for the audience (tracked)
```

`.source/`, `draft/`, `.scratchpads/`, and `.outputs/` work exactly as in an
ordinary sub-workspace — see `docs/howto-workspace-conventions.md`. The
frame-scoped addition is `.context/`.

### `.context/` — curated, frame-filtered crawl entrypoint

Stable, reusable, frame-tagged. Distinct from `.scratchpads/` (intermediate,
gitignored) and from `draft/` (your narratives, audience-facing).

Required files:

- **`index.md`** — short crawl entrypoint; lists the other files with a
  one-line "what to use it for" each.
- **`frame.md`** — the audience, scope, and explicit "what this is NOT".
- **`people.md`** — translation table for shared entities; per-frame role mapping.
- **`timeline.md`** — frame-native phasing + translation to other frames' phasing.
- **`references.md`** — explicit whitelist of cross-workspace paths with
  frame-shift notes ("use for this frame: …; do NOT pull: …").

Add a frame-relevant metric anchor file (`unit-economics.md`, or whatever the
quantitative spine is) when the frame has one.

Each file leads with a frame statement: *"Frame: \<frame name\>. Audience:
\<audience\>. What this is NOT: \<adjacent frame\>."* This is non-negotiable.

## Cross-workspace handling — move / copy / reference decision tree

| Situation | Action |
|---|---|
| File is **only** relevant to this frame | **Move** (`git mv`) into the frame workspace |
| File is canonical for multiple frames AND framing-shifted (a person's role differs by frame) | Curate the **frame-shifted view** in `.context/people.md`; **reference** the upstream file in `.context/references.md`; do NOT copy the file |
| File is canonical for multiple frames AND framing-stable | **Reference** in `.context/references.md`; do NOT copy or move |
| File is at risk of drifting if duplicated (evolving canonical docs) | **Reference** — never copy. Symlinks are fragile in git; markdown references work everywhere |
| File is sensitive (honest assessments, credentials) | Place in `.scratchpads/` (gitignored), not `.source/` |

Never `cp` a canonical file into the new workspace just to make synthesis
easier. The cost is silent drift when the original is updated and the copy
isn't. Use a reference + a frame-shift note instead.

## Frame-shift translation discipline

Two files do most of the work:

- **`.context/people.md`** — translation table, one row per shared entity, a
  column for each frame they appear in.
- **`.context/timeline.md`** — frame-native phase labels with a translation
  table to neighbouring frames.

When about to refer to a shared entity in an artefact, the discipline is:

1. Look up the entity in `.context/people.md`.
2. Use the row's *this-frame* column.
3. If the entity is not in the table, **stop and ask the human** — that's a
   signal of either (a) a frame-shift about to happen silently, or (b) a new
   entity that needs adding to the table.

## Drift-prevention mechanisms

1. **Frame statement at file top** — every `.context/`, `.source/`, `draft/`
   file leads with frame + audience + "what this is NOT".
2. **Translation tables** in `.context/people.md` and `.context/timeline.md`.
3. **CLAUDE.md whitelist + blacklist** — the workspace's `CLAUDE.md` lists
   cross-workspace paths it may crawl, and framings that must NOT be imported
   even from whitelisted paths.
4. **Pause-points for the human** — ask before: pulling content from another
   workspace, detecting a frame-shift on a shared entity, or adding a new entry
   to `references.md`.
5. **Pre-render check** — every render reads canonical markdown, never the
   rendered binary.

## When to apply this pattern

Apply when:

- The same content must serve **two distinct audiences** with framing
  differences.
- A single workspace contains **conflicting representations** of the same
  entity (a person's role, a phase, a number).
- Synthesis quality is degrading — the wrong context is leaking into artefacts.

Do NOT apply when:

- The workspace serves a single audience and a single framing — the overhead of
  `.context/` is wasted ceremony. Use an ordinary sub-workspace.
- The work is short-term tactical (a one-off report, a single check-in) — that's
  a leaf-doc, not a workspace.

## Anti-patterns

- **Copying canonical files instead of referencing** — silent drift the moment
  upstream changes.
- **Symlinks across workspaces** — fragile across OS / git / IDE; use markdown
  references in `.context/references.md` instead.
- **Skipping the translation table** — without `.context/people.md` and
  `.context/timeline.md`, frame-shifts happen silently.
- **Treating `.source/` as editable** — it is read-only by convention; editing
  the upstream file breaks provenance.
- **Letting `.context/index.md` grow long** — it's an index; keep it short and
  scannable. Long content goes in the files it indexes.

## Related

- `docs/howto-workspace-conventions.md` — the ordinary sub-workspace zones this
  pattern extends.
- `docs/howto-set-up-frame-scoped-workspace.md` — step-by-step recipe to create
  a new frame-scoped workspace.
