# Workspace OS specification

Status: Approved for phased implementation on 2026-07-12.
Stream: `workspace-os`.
Research inputs:

- harness comparison matrix
- information-organisation research note
- index-format spike notes
- approved workspace-OS phase plan

## Goals

`cc-ide-workspace` should evolve from an IDE-first template into a
harness-agnostic **workspace OS**: a folder that carries instructions, memory,
policies, routines, indexes, generated artifacts, and tool configuration. The
pitch should stay simple: clone the template, open the folder in an IDE, chat.

The workspace should support consulting-style work:

- per-client or per-engagement folders;
- multiple workstreams;
- raw inputs, distilled context, and generated outputs;
- agendas, briefs, meeting notes, check-ins, invoices, and share packs derived
  from the same source material;
- guardrails for scope, confidentiality, and contract boundaries;
- interchangeable agent harnesses: Codex, Claude Code, opencode, pi, Hermes, and
  future runtimes with thin adapters.

## Non-goals

- No central database in the template core.
- No mandatory web UI.
- No mandatory runtime beyond git, an IDE, the selected agent harness, and the
  current Python/uv baseline.
- No attempt to make hooks judge semantic consulting scope. Scope judgment stays
  prose plus reviewable registers.
- No full migration of existing downstream workspaces in this spec phase.
- No spec-compiler framework. Adapter generation should be boring file rendering
  with content hashes.

## Entity model

The workspace uses a closed vocabulary at first:

| Entity | Meaning |
|---|---|
| Workstream | A bounded body of client/project work with its own sources, prep, outputs, and generated indexes. |
| Meeting | A scheduled or completed conversation, usually with prep, transcript, notes, and follow-ups. |
| Person | A participant, stakeholder, owner, or contact. |
| Source | Canonical input material: client docs, recordings, exported data, reference files. |
| Artifact | A generated or authored deliverable: brief, deck, agenda, memo, invoice, analysis. |
| Decision | A chosen direction with rationale, date, actors, and supersession links. |
| Learning | Reusable distilled knowledge, convention, or pattern. |
| Routine | A repeated workflow that may graduate into a skill, script, or app. |
| Session | A conversation/work session with an agent or human collaborator. |
| Policy | A rule or boundary, including scope, sharing, security, and workflow policy. |

Relations follow PROV-O-style vocabulary where possible:

- `wasDerivedFrom`
- `wasGeneratedBy`
- `references`
- `about`
- `partOf`
- `supersedes`

## Directory taxonomy

This is the target v2 layout. The specification PR does not create these paths;
the roadmap adds them in separate Phase 3 branches while preserving the current
v1 layout until each migration lands.

Root:

```text
AGENTS.md
README.md
_inbox/
journal/
memory/
policies/
workspace/
scripts/
apps/
.agents/
.codex/
.claude/
.opencode/
.sessions/
.local/
```

Workstream:

```text
workspace/<workstream>/
  source/
  prep/
  outputs/
  scratchpad/
  .local/
  _index.jsonld
  _TOC.md
  _STATUS.md
```

Definitions:

- `_inbox/`: capture point for unsorted files and notes. Triage moves or links
  material into workstreams and records unresolved items.
- `journal/`: date-partitioned distilled event log, e.g. `journal/2026/07/`.
  This is the time-range retrieval layer.
- `memory/`: workspace-resident memory: small always-on summaries, learning
  notes, and routine records. High-detail procedures should become skills.
- `policies/`: scope, sharing, MCP, secrets, and generated-adapter policy.
  Contract-specific policy may live under `policies/contract/` and be gitignored
  when needed.
- `workspace/<workstream>/source/`: canonical inputs.
- `workspace/<workstream>/prep/`: agendas, prep notes, planning material.
- `workspace/<workstream>/outputs/`: generated or delivered artifacts.
- `workspace/<workstream>/scratchpad/`: working drafts and temporary notes,
  required to be gitignored when the workstream layout is introduced.
- `workspace/<workstream>/.local/`: private operational context for that
  workstream, also required to be gitignored during that migration.

## Metadata and indexes

ADR-001 and ADR-003 decide the index architecture:

- canonical metadata lives in frontmatter next to artifacts;
- generated files are derived from a disk scan;
- catalogs, TOCs, dashboards, and typed views are never hand-maintained;
- generated files include stamps/content hashes;
- disk scanning uses an explicit skip-list, not an extension whitelist.

Example metadata:

```yaml
---
type: decision
title: "Decision: SvelteKit for the Acme marketing site"
date: 2026-06-18
status: final
workstream: acme-rebrand
people: [alex, riley]
references:
  - research/2026-06-15-ui-framework-options.md
wasDerivedFrom:
  - meetings/2026-06-09-kickoff.notes.md
confidentiality: client
---
```

The entity `id` is not authored in frontmatter: it IS the workstream-relative
path (here `decisions/2026-06-18-ui-framework.md`), assigned by the generator.
This matches the spike recommendation, keeps ids unique and grep-resolvable by
construction, and makes renames explicit graph events.

Generated outputs:

- per-workstream `_index.jsonld`;
- per-workstream `_TOC.md`;
- per-workstream `_STATUS.md`;
- root aggregate `_STATUS.md`;
- optional typed modules/views for richer querying.

## Blocking and advisory checks

| Check | Timing | Severity | Rationale |
|---|---|---|---|
| Invalid metadata schema | Commit gate | Block | Generated views cannot be trusted. |
| Dangling required references | Commit gate | Block | Provenance graph is broken. |
| Stale generated adapters | Commit gate | Block | Harnesses would run divergent rules. |
| Secret files in tracked/shareable paths | Commit gate | Block | Prevent obvious data leaks. |
| Files tracked from private capture paths | Commit gate | Block | Raw screenshots, traces, and scratch material are private by default. |
| New binary/media artifacts | Pre-share check | Advise and require manual review | Text scanning cannot inspect pixels or embedded metadata. |
| Workspace path confinement violations | Runtime hook/adapter | Block | Prevent tools from touching unrelated folders. |
| Missing optional metadata | SessionStart/status | Advise | Useful hygiene, but should not stop work. |
| Orphaned files | SessionStart/status | Advise | Some files may be intentionally temporary. |
| Stale summaries | SessionStart/status | Advise | Review prompt, not a hard failure. |
| Low catalog coverage | SessionStart/status | Advise until generator exists | Drift signal; becomes block only for required generated catalogs. |

## Adapter model

The workspace has one canonical harness-neutral spec. ADR-004 chooses root
`AGENTS.md` as the canonical instruction file.

Generated adapters:

| Harness | Adapter output |
|---|---|
| Codex | `AGENTS.md`, `.codex/hooks.json`, `.codex/hooks/`, optional skills/config. |
| Claude Code | `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/`, `.claude/skills/`. |
| opencode | `opencode.json`/`.opencode/` with `instructions`, permissions, MCP, commands/plugins as needed. |
| pi | `.pi/settings.json`, optional `.pi/extensions/workspace-policy.ts`, prompt templates. |
| Hermes | optional `.hermes.md`, `HERMES_HOME` guidance, config fragment for skills/hooks/MCP/cron. |
| Odysseus | future importer/provider, not a Phase 3 core adapter. |

Generated adapter files should carry:

- source file list;
- generator version;
- content hash;
- "do not edit by hand" header;
- regeneration command.

If a generated adapter is edited or stale, the commit gate blocks until it is
regenerated or the canonical source changes.

## Memory and reflection

Memory is workspace-resident, not hidden in one harness by default.

Layers:

- `memory/index.md`: small, always-on map of what exists.
- `memory/core.md`: bounded facts that should be loaded often.
- `memory/learnings/`: reusable learned patterns and decisions.
- `.agents/skills/` or `.claude/skills/`: procedural memory with progressive
  disclosure.
- `.sessions/`: task continuity and compaction recovery.

`/reflect` should route to repo memory when a `memory/` directory exists:

1. capture a session summary into `.sessions/`;
2. update bounded memory only for durable facts;
3. update or draft skills for repeated procedures;
4. record unresolved scope/contract issues in policy registers.

Auto-learning should create drafts or patches, not silently rewrite canonical
memory without git review.

## Scope and contract guardrails

Semantic scope judgment cannot be enforced perfectly by hooks. The honest
boundary is:

- prose policy in `policies/scope.yml` and `AGENTS.md`;
- SessionStart injects a brief scope summary;
- a `/scope` skill checks a user ask against known scope, cites the policy, and
  appends ambiguous/out-of-scope items to a register;
- hooks block only structural boundaries, such as forbidden paths, tracked
  secrets, and stale policy adapters.

Guiding rule: capture out-of-scope material without absorbing it into the active
workstream unless the user explicitly accepts the scope change.

## Meeting pipeline

Meeting artifacts use the same slug:

```text
prep/2026-07-15-client-checkin.agenda.md
source/2026-07-15-client-checkin.recording.m4a
source/2026-07-15-client-checkin.transcript.md
outputs/2026-07-15-client-checkin.notes.md
journal/2026/07/2026-07-15-client-checkin.md
```

The notes skill should:

- read prep, transcript, roster, and relevant memory;
- create notes and follow-ups;
- append a distilled journal event;
- update generated indexes;
- propose learning/routine updates if the workflow repeated.

## Artifact skills and query layer

User-facing skills such as `/brief`, `/agenda`, `/invoice`, and `/checkin-prep`
should use one query layer over journal plus generated catalogs.

Inputs:

- date range;
- workstream/client;
- artifact type;
- person/stakeholder;
- confidentiality/share profile.

The current v1 default remains `workspace/.outputs/`. When the Phase 3
workstream migration lands, the default becomes
`workspace/<workstream>/outputs/` unless the user specifies another destination.

## Sharing

Share packs should be deterministic zips created from policy:

- include selected workstreams, generated catalogs, and deliverables;
- exclude `.local/`, scratchpads, credentials, raw private sessions, and
  policy-marked non-shareable files;
- treat screenshots, browser traces, PDFs, Office documents, and recordings as
  private until a sanitized derivative is explicitly approved for the audience;
- include a manifest of included/excluded paths and reasons;
- include enough memory/policy context for a recipient agent to answer "query my
  mind" questions within the shared scope.

Config belongs in `policies/sharing.yml`.

Until share packs exist, `scripts/src/workspace_check.py` is the minimum
pre-commit/pre-share gate. It intentionally does not replace manual review of
binary files. See `docs/howto-share-safely.md`.

## MCP and credentials

There should be one canonical MCP registry with slug placeholders and secret
references. Generated harness adapters consume it.

Rules:

- secrets live in `.local/credentials/`, environment variables, or an external
  secret manager;
- committed config uses placeholders only;
- MCP server schemas are treated as untrusted input and length-capped when
  rendered into prompts;
- per-workspace adapters disable external sharing by default for client work.

## Console

`~/space/ctl` should stay thin:

- `ctl ws new`: clone template, substitute slugs, initialize git, run smoke
  checks.
- `ctl ws status`: aggregate each instance's generated status JSON.
- No central DB.
- No web UI until at least three real instances prove the shape.

The folder is the tenant. The console provisions and summarizes; it does not own
the workspace's source of truth.

## Implementation roadmap

Deferred implementation tasks live in
`docs/roadmap-workspace-os.md`. The spec defines the target architecture; the
roadmap is the master list for separate, testable branches.

## Target success tests

- Fresh clone works with the PM pitch: open IDE, chat, no manual runtime hunt.
- Codex/Claude/opencode read the same canonical instructions through adapters.
- `/invoice 2026-06-01..2026-06-30` can draft from journal and generated catalog
  data without a database.
- Share pack excludes `.local/`, scratchpads, and secrets.
- Blocking checks remain enabled after real usage, because they block only crisp
  structural failures.
