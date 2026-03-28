# Pattern: The .local/ Directory

`.local/` is the third layer of the workspace's continuity model. While code lives in git and session logs capture decisions, `.local/` holds the operational context — everything Claude needs to work effectively that shouldn't be committed.

## The three-layer model

```
Layer 1: Code (git)       → what exists now
Layer 2: .sessions/       → why it was built, what was tried, what's next
Layer 3: .local/          → how to operate it (prompts, runbooks, credentials, evidence)
```

Claude reads all three layers when starting a session. `.local/` provides the "how" that code and session logs don't capture.

## Content categories

### Credentials and secrets
Files that reference what secrets are needed and where — structure without committing actual values.

```
.local/
├── api-keys.md               # Which API keys are needed, where to get them
├── credentials.env            # Actual keys (never commit)
└── service-accounts.md        # Service account setup notes
```

### Analysis and planning
Assessments and plans too detailed or volatile for git, but critical for execution.

```
.local/
├── ANALYSIS_SUMMARY.md        # Current state assessment, confidence levels, action plan
├── PRE_PLAN.md                # Deployment runbook, infrastructure map, phase gates
└── SPEC.md                    # Living spec, evolving faster than git commits
```

### AI system prompts
Prompt templates and persona protocols that Claude references and iterates on.

```
.local/
├── prompts/
│   ├── analysis-prompt.txt    # Data analysis prompt template
│   └── persona-protocol.txt   # Conversation persona definition
```

### Screenshots and QA evidence
Visual proof of completed features, regression testing results.

```
.local/
├── screenshots/
│   ├── feature-dashboard.png
│   └── mobile-responsive.png
└── qa-test/
    ├── test-run-2026-03-27.png
    └── regression-results.md
```

### Reference data
External data relevant to the project but not code — PDFs, exports, reports.

```
.local/
├── legal-requirements.pdf
├── google-drive-inventory.json
└── competitor-analysis.html
```

### Working notes
Living documents too volatile for git, too important to lose.

```
.local/
├── RESOURCES.md               # Links, references, bookmarks
├── DECISIONS.md               # Architecture decisions not yet finalized
└── security-audit-notes.md    # Investigation in progress
```

## Rules

- **Never commit** — `.local/` is gitignored. This is by design.
- **Never delete** — Minify old content instead of deleting. Compress to essentials.
- **Check for credentials** — Before referencing `.local/` content in conversation output, verify it doesn't contain secrets.
- **Translate valuable content** — When analysis or decisions stabilize, move them to `docs/` (committed) or `workspace/` (user-facing).

## First-use bootstrapping

When you first clone this workspace, `.local/` is empty (just a `.gitkeep`). On your first Claude session, Claude will create a `GUIDE.md` in `.local/` with these categories and examples, tailored to your project.

## Scale in practice

In active projects, `.local/` grows significantly:
- 40+ files across categories
- 5+ MB of operational context (screenshots, PDFs, exports)
- Multiple subdirectories for organization

This is expected and healthy — it means Claude has rich operational context for every session.
