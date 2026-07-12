# ADR-001: Index format and language

Status: Accepted.
Date: 2026-07-04

## Context

The workspace needs indexes that humans can browse, agents can grep, and tools
can validate. A downstream workspace showed the failure mode: hand-maintained
catalogs and TOCs drift in busy folders, especially when advisory checks are
ignored.

The index-format spike modeled one sample workstream four ways:

- Markdown frontmatter plus generated `_index.jsonld` and `_TOC.md`;
- hand-authored TypeScript modules run by Bun;
- hand-authored Python dataclass/dict modules run by uv;
- the hybrid under decision, built as `variant-d-hybrid/`: frontmatter as
  source of truth, a stdlib Python generator emitting a GENERATED typed
  TypeScript module (`index.gen.ts`, content-hash header, blocking
  validation), and hand-written expressive views (`views.ts`: `toc`,
  `brief --since --until`) run by Bun.

## Decision

Use **artifact-local Markdown frontmatter as canonical metadata**, with
generated catalogs and views.

Code is allowed for:

- schema definitions;
- validators;
- generators;
- typed view/query helpers;
- optional generated TypeScript modules.

Code is not the canonical data format for workstream indexes.

Required generator runtime: `uv run python3` using stdlib-first code.
Optional view runtime: Bun/TypeScript, only after fresh-clone smoke tests prove
the install story.

## Consequences

Positive:

- Humans see metadata where the artifact lives.
- Grep-only agents can inspect metadata without executing code.
- A bad metadata edit usually affects one file, not the whole catalog.
- Generated JSON-LD can carry graph/provenance relations.
- Typed views can still satisfy the "self-expressive structured docs" goal
  without owning canonical facts.

Negative:

- Frontmatter needs strict validation.
- More generator work is required.
- Some expressive authoring moves from data files into generated views.

## Verification

The spike verified that all four variants can answer the sample date-range
query. Frontmatter plus generation (A) scored highest of the hand-authored
options on drift resistance, human browsability, agent edit ergonomics, BYOM
greppability, and install story. The hybrid (D) was then built to test — not
presume — this decision: it kept every one of A's scores (identical canonical
data surface) while its hand-written typed views rendered a period brief with
provenance chains, superseded-filtering, and decider annotations in ~40 lines
of autocomplete-checked TypeScript. Scores and transcript:
hybrid D totals 33/35 vs A's 32, trading one install-story point for the
self-expressiveness the user wanted.
