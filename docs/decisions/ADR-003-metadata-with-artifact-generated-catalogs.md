# ADR-003: Metadata with artifacts, generated catalogs

Status: Accepted.
Date: 2026-07-04

## Context

The workspace must serve both humans and agents. Humans browse folders and open
files. Agents grep, read metadata, and call generated query tools. Maintaining a
separate hand-written catalog creates drift: files get added, renamed, and
superseded faster than catalog tables are updated.

## Decision

Store canonical metadata with the artifact, then generate catalogs.

Required generated outputs:

- per-workstream `_index.jsonld`;
- per-workstream `_TOC.md`;
- per-workstream `_STATUS.md`;
- root aggregate status.

The generator scans disk minus an explicit skip-list. It must not use a narrow
extension whitelist, because office documents, diagrams, transcripts, and
exports all matter.

## Consequences

Positive:

- Folder browsing and structured querying share the same source.
- Generated status can expose drift without becoming another hand-maintained
  surface.
- JSON-LD gives a graph-friendly export without forcing humans to author JSON-LD.

Negative:

- Every artifact type needs a metadata schema.
- Legacy/unstructured files need triage or explicit exemptions.
- The generator must be fast enough for hooks and session-start checks.

## Blocking rules

Block commits for invalid required metadata, dangling required refs, stale
generated outputs, and generated-adapter staleness.

Advise for missing optional metadata, orphaned files, stale summaries, and low
coverage until the user decides those should graduate to blockers.
