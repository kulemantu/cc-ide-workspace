# Pattern: CLI Scripts

When you find yourself asking Claude the same thing repeatedly, the natural evolution is a script. These scripts live in `scripts/src/` and are designed to be called both by you and by Claude.

## When to build a script

If you've asked Claude the same thing 3+ times, it's time for a script. Common triggers:

- "Set up the dev environment"
- "Seed the database with test data"
- "Run the smoke tests"
- "Generate a report from this data"
- "Check if the deploy worked"

## Where scripts live

| Location | When to use |
|----------|-------------|
| `scripts/src/` | Reusable code — modules, utilities, CLI tools |
| `.local/` | One-off scratch scripts — experiments, quick hacks |

Scripts graduate from `.local/` to `scripts/src/` when they prove useful across sessions.

## Script conventions

Claude writes scripts with these traits:

**`--help` descriptions** — Every script should have clear help text. This isn't just for humans — Claude itself reads `--help` output to understand what a script does and how to call it.

```python
import argparse

parser = argparse.ArgumentParser(
    description="Seed the database with example data for testing"
)
parser.add_argument("--dry-run", action="store_true", help="Show what would be seeded without writing")
parser.add_argument("--count", type=int, default=10, help="Number of records to create")
```

**Idempotent** — Safe to run repeatedly. If the data already exists, skip it. If the service is already running, report it.

**Dry-run mode** — Show what would happen before doing it. This is a natural Claude Code interaction pattern: "Show me what this will do before doing it."

**Colored output** — `[INFO]`, `[ERROR]`, `[SUCCESS]` markers for readable terminal output.

**Zero or minimal dependencies** — Prefer Python stdlib. When external deps are needed, add them to `scripts/pyproject.toml` via `uv add`.

## Testing

Every script in `scripts/src/` gets a corresponding test in `scripts/tests/`. Claude writes these automatically — it's enforced by the Python tooling rule.

## Example patterns

| Pattern | What it does |
|---------|-------------|
| Data seeding | Create test records with `--dry-run` and `--count` flags |
| Environment setup | Check/install prerequisites, create configs, verify health |
| Smoke tests | Hit API endpoints, verify responses, report pass/fail |
| Report generation | Read input from `workspace/`, write output to `workspace/outputs/` |
| Database migration | Transform data with preview mode and rollback support |

## Key insight: scripts for AI agents

The `--help` flag matters doubly in this workspace. When Claude encounters a script, it reads `--help` to understand the interface. Well-documented CLI scripts become tools that Claude can compose — calling one script's output as another's input.

This means your scripts aren't just automation — they're an API that Claude can use autonomously.
