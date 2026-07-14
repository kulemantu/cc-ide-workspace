# Pattern: Scripts from Repeated Prompting

When you ask Claude the same thing repeatedly — "deploy this," "seed the database," "run the smoke tests" — the natural evolution is to extract that into a script. These scripts are artifacts of Claude Code usage patterns, crystallized into reusable automation.

> **Prerequisite:** Before reaching for a script, work through the [task escalation ladder](pattern-task-escalation.md). Scripting is Tier 3 — only after model context (Tier 0), existing CLI tools (Tier 1), and new CLI tools (Tier 2) have been considered. Claude tracks repeated operations as "routines" in memory and escalates suggestions over time.

## The lifecycle

```
Repeated prompt → One-off script (.local/) → Reusable module (scripts/src/) → Tested CLI tool
```

1. **Repeated prompt**: Claude has tracked the same routine 3+ times via memory
2. **One-off script**: Claude writes a quick script in `.local/` to automate it (with user approval)
3. **Reusable module**: The script proves useful, moves to `scripts/src/`
4. **Tested CLI tool**: Claude adds argparse, `--help`, `--dry-run`, and tests

## Common script categories

| Category | Origin prompt | Example |
|----------|--------------|---------|
| Environment setup | "Set up the dev environment" | Config generation, service startup, health checks |
| Data seeding | "Seed the database with test data" | Idempotent record creation with `--dry-run` |
| Integration tests | "Check if the deploy worked" | API endpoint health checks, webhook verification |
| Report generation | "Generate a summary of this data" | Read from `workspace/`, write to `workspace/<subfolder>/.outputs/` |
| Auth setup | "Configure Keycloak for this service" | Token acquisition, role creation, mapper config |
| Multi-repo coordination | "Commit these changes across both repos" | Batched conventional commits across directories |

## Common traits

Scripts born from repeated prompting share these characteristics:

| Trait | Why |
|-------|-----|
| **Idempotent** | Claude was asked to "set up X" multiple times — the script handles already-existing state |
| **Dry-run mode** | "Show me what this will do before doing it" — a natural Claude interaction pattern |
| **`--help` documentation** | Claude reads `--help` to understand scripts it wrote in previous sessions |
| **Colored output** | `[INFO]`, `[ERROR]`, `[SUCCESS]` — readable status in the terminal |
| **Environment-first config** | `.env` files and env vars — Claude reads `.env` for context |
| **Minimal dependencies** | Python stdlib where possible — no extra install steps |

## When to extract a script

Ask yourself: "Have I asked Claude to do this before?"

- **Once**: Just let Claude do it interactively
- **Twice**: Note the pattern, maybe save the approach in a session file
- **Three times**: Time for a script. Ask Claude: *"This is the third time I've asked for this — let's make it a reusable script"*

## In this workspace

- One-off scripts start in `.local/` (gitignored, scratch)
- Proven scripts graduate to `scripts/src/` (committed, tested)
- Every script in `scripts/src/` gets tests in `scripts/tests/`
- Output always goes to `workspace/<subfolder>/.outputs/`
