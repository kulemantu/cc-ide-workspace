# ADR-002: Evolve this repository in place

Status: Accepted.
Date: 2026-07-04

## Context

The user confirmed that v2 should live in `cc-ide-workspace`, not in a new
repository. The repository is already the template users clone, and recent
downstream-to-upstream work has proven that generic conventions can be folded
back into it.

The main risk is breaking existing users or instances that depend on the current
shape.

## Decision

Evolve `cc-ide-workspace` in place, with branch-per-phase changes and a `v1` tag
before build-phase merges.

The spec phase adds documentation only. Build phases should be split by concern:

- adapter generation and canonical instruction files;
- workspace indexing and journal;
- share packs, policy skeleton, and console commands;
- pilot migration.

## Consequences

Positive:

- The template remains the product.
- Existing docs, hooks, scripts, and apps stay close to the source of truth.
- Changes can be piloted through normal git review.

Negative:

- The repo will carry transitional compatibility surfaces.
- Build phases need disciplined commits and migration notes.
- Existing downstream users need a v1 anchor before disruptive layout work.

## Follow-up

Before Phase 3 lands, tag the current stable template as `v1` and write a short
migration note for instances that want to adopt workspace-OS conventions.
