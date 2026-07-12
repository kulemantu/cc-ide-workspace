# How to share workspace material safely

Treat workspace content as private until the user names both the material and
the destination. Gitignore reduces accidents; it is not consent to share.

## One pre-share workflow

From the repository root, run the complete local gate:

```bash
uv run --project scripts python3 scripts/src/workspace_check.py verify
```

Before committing or attaching a smaller staged change, inspect only that set:

```bash
git diff --cached --name-status
uv run --project scripts python3 scripts/src/workspace_check.py hygiene --staged
```

`BLOCK` findings must be fixed. `WARN` findings require a human to inspect the
actual file; the tool cannot determine whether pixels, document properties, or
embedded media disclose client information. After reviewing every warned file,
record that acknowledgment explicitly:

```bash
uv run --project scripts python3 scripts/src/workspace_check.py hygiene --staged --allow-reviewed-media
```

Use the same `--allow-reviewed-media` option with `verify` only after completing
that review.

## Screenshots and browser captures

Raw captures start in `.local/screenshots/`, never in a tracked folder. Browser
automation output stays in `.playwright-mcp/`, `test-results/`, or
`playwright-report/`; these paths are ignored by default.

Before sharing a derived screenshot:

1. Crop to the smallest area that proves the point.
2. Remove tabs, URLs, notifications, account avatars, emails, client names,
   tokens, IDs, and unrelated records.
3. Check the whole image at full resolution, not only the intended focal area.
4. Export a sanitized copy; do not overwrite the raw evidence.
5. Confirm the destination and audience with the user before attaching or
   uploading it.

Prefer text logs or a minimal reproduction when a screenshot adds no necessary
evidence. Public-repository issue and PR attachments must be treated as public.

## Documents and generated outputs

- Use fictional names and placeholders in public examples.
- Do not quote contract terms, amounts, credentials, personal data, private URLs,
  or client identifiers without explicit approval.
- Keep raw exports, signed documents, recordings, and evidence under `.local/`.
- Put a sanitized, approved derivative in `workspace/.outputs/` only when it is
  ready for the named audience.
- Review frontmatter and filenames as well as body text; metadata can disclose
  the same information as prose.

## What the check does not prove

`workspace_check.py` catches private path violations, credential-shaped
filenames, and a small set of high-confidence secret patterns. It does not OCR
images, inspect Office/PDF internals, remove EXIF data, classify legal
confidentiality, or authorize sharing. Those remain explicit review steps.

If a sensitive file was tracked previously, adding it to `.gitignore` is not
enough: verify with `git ls-files <path>` and handle repository-history cleanup
as a separate incident.
