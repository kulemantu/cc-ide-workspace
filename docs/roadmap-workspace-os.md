# Workspace OS roadmap

Status: Deferred implementation list for the workspace-OS spec.

This roadmap keeps future implementation work out of the architecture spec. The
current PR can be tested end to end as documentation, app discovery, and
fresh-clone tooling.
Implementation tasks below should become separate branches with their own tests.

## Included in the specification PR

- App and skill discovery docs:
  - `apps/` is documented as the home for self-contained shareable CLIs.
  - `.claude/skills/transcribe.md` wraps the transcriber app as a thin command.
  - App usage consistently uses `uv run python3`.
- Workspace-OS specification and ADRs:
  - `docs/spec-workspace-os.md`
  - `docs/decisions/ADR-001-index-format-and-language.md`
  - `docs/decisions/ADR-002-evolve-in-place.md`
  - `docs/decisions/ADR-003-metadata-with-artifact-generated-catalogs.md`
  - `docs/decisions/ADR-004-canonical-agent-spec-file.md`
- Fresh-clone script checks:
  - `scripts/` is a non-package uv environment.
  - `uv run pytest` has a template smoke test instead of failing with "no tests
    collected".

## Verification for current branch

Run from the repository root unless noted:

```bash
cd scripts && uv run pytest
cd scripts && uv run ruff check .
cd scripts && uv run pyright
cd apps/transcriber-prioritizer && uv run python3 -m unittest test_transcribe_call -v
```

Expected results:

- `pytest`, `ruff`, `pyright`, and app unittest pass.

## Deferred master list

### 1. Adapter generation

Build `scripts/src/agents_sync.py` with tests.

Success criteria:

- Root `AGENTS.md` is the canonical source.
- Generated `CLAUDE.md`, `.codex/`, and opencode adapter include source hashes.
- Commit gate blocks stale generated adapters.
- Fresh clone can regenerate adapters deterministically.

### 2. Workspace indexer

Build `scripts/src/wsindex/` from artifact-local frontmatter.

Success criteria:

- Generates per-workstream `_index.jsonld`, `_TOC.md`, and `_STATUS.md`.
- Scans disk with an explicit skip-list, not an extension whitelist.
- Blocks invalid required metadata and dangling required references.
- Provides a date-range query over generated catalogs.

### 3. Journal and inbox workflow

Add root `_inbox/` and `journal/` conventions, plus the first workflow skill that
uses them.

Success criteria:

- Inbox triage produces or updates metadata.
- Meeting notes append a distilled journal entry.
- Date-range retrieval works without a database.

### 4. Repo-resident memory

Create the first `memory/` skeleton and route reflection into it.

Success criteria:

- Bounded always-on memory is separated from procedural skills.
- Reflection updates `.sessions/` and drafts memory/skill changes without
  silently rewriting canonical files.
- No harness-private memory is required for a fresh clone to understand the
  workspace.

### 5. Policies and share packs

Add `policies/` skeleton and `scripts/src/sharepack.py`.

Success criteria:

- Share pack excludes `.local/`, scratchpads, credentials, and private sessions.
- Share manifest lists included and excluded paths with reasons.
- Policy checks distinguish blocking structural failures from advisory workflow
  hygiene.

### 6. MCP registry

Add a canonical MCP registry with secret placeholders and generated harness
adapters.

Success criteria:

- Committed config contains placeholders only.
- Generated harness config never contains secret values.
- MCP schemas are treated as untrusted input when rendered into prompts.

### 7. Provisioning console

Keep the console thin: clone, substitute slugs, run smoke checks, and aggregate
status JSON.

Success criteria:

- New workspace instances are folder-owned tenants, not rows in a central DB.
- Status aggregation reads generated status, not private harness state.
- No web UI until at least three real child workspaces prove the shape.

### 8. Pilot and child-template comparison

Use real child workspaces to compare the template against lived practice.

Comparison checklist:

- Which generated files changed from the template, and why?
- Which local conventions appeared in multiple children?
- Which checks were disabled or bypassed?
- Which inbox/journal/memory routines survived two weeks of use?
- Which artifacts could be produced from generated catalogs without a database?
- Which private or client-specific terms would leak if the child were upstreamed?

Outputs:

- a short comparison note per child workspace;
- candidate upstream changes grouped by concern;
- rejected child-specific conventions with reasons.
