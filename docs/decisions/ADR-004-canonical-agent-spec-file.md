# ADR-004: Canonical agent spec file

Status: Accepted.
Date: 2026-07-04

## Context

The workspace should run under multiple harnesses without copying and editing
parallel instruction files by hand. Current evidence:

- Codex reads `AGENTS.md`.
- opencode reads `AGENTS.md` and can also consume Claude-compatible skills.
- pi reads `AGENTS.md` or `CLAUDE.md`.
- Hermes reads `AGENTS.md` after its own harness-specific files.
- Claude Code currently uses `CLAUDE.md`.

The plan needs a canonical source that can generate harness-specific adapters
and prevent stale sed-mangled copies.

## Decision

Use root `AGENTS.md` as the canonical harness-neutral agent spec.

Generate harness-specific outputs from it:

- `CLAUDE.md` for Claude Code;
- `.codex/` config and hooks for Codex;
- opencode config and optional `.opencode/` resources;
- pi and Hermes adapters when those phases begin.

Harness-specific deltas should live in small adapter templates, not in the
canonical prose.

## Consequences

Positive:

- Aligns with the emerging open convention.
- Works natively for Codex and opencode.
- Gives this repo one file to review for policy drift.
- Makes stale adapter detection straightforward.

Negative:

- Claude Code remains a generated compatibility surface until it reads
  `AGENTS.md` natively.
- Existing docs and hooks that mention `.claude/` need migration care.
- The generator must preserve local harness affordances without bloating
  `AGENTS.md`.

## Adapter staleness

Generated adapters must include a source hash. The commit gate blocks if a
generated adapter is stale relative to canonical `AGENTS.md` or its template.
