# How to: Hooks

Hooks are deterministic guardrails that enforce workspace conventions automatically. Instead of relying on Claude to remember every rule, hooks intercept tool calls and fire scripts that block, approve, or modify actions.

## What's included

This workspace ships with 4 hooks in `.claude/hooks/`, wired via `.claude/settings.json`:

| Hook | Event | What it does |
|------|-------|-------------|
| `pre_bash_check.py` | PreToolUse (Bash) | Unified check: blocks bare `python` (requires `uv run`), blocks `rm` on protected dirs, validates conventional commits, forces push approval |
| `auto_format_python.py` | PostToolUse (Edit\|Write) | Runs `ruff format` after Python file edits |
| `pre_compact_session_reminder.py` | PreCompact | Reminds to update `.sessions/` before context compaction |
| `session_start_context.py` | SessionStart | Injects three-layer continuity context on startup |

The four Bash PreToolUse checks (uv enforcement, workspace protection, commit format, push approval) are consolidated into a single `pre_bash_check.py` to avoid multiple hook evaluations per Bash call. Each hook maps to a rule in `.claude/rules/` — they enforce what's already documented, not new policy.

## How hooks work

Hooks are Python scripts that:
1. Read JSON from stdin (contains tool name, arguments, and context)
2. Decide whether to allow, block, or modify the action
3. Exit with a code: `0` = allow, `2` = block (stderr message shown to Claude)

The wiring in `.claude/settings.json` controls which events trigger which scripts. The `matcher` field filters by tool name.

## Design decisions

**Python, not shell.** The workspace rule is "always Python, never bash scripts" — hooks follow the same convention. Python is more readable, testable, and maintainable for anyone reviewing the repo.

**System Python (`python3`), not `uv run`.** Hooks are infrastructure, not project code. They use only stdlib (`json`, `re`, `sys`, `os`, `pathlib`, `subprocess`) and must complete in under 100ms. Running through `uv` would add unnecessary startup time.

**`$CLAUDE_PROJECT_DIR` for all paths.** No hardcoded user paths. Every script references the project root via the environment variable Claude Code provides.

**No user-specific conventions.** Hooks don't validate sign-off lines, co-author trailers, or personal preferences. Those belong in `~/.claude/rules/` per user. The hooks enforce only what's in the repo's `.claude/rules/`.

## Testing hooks manually

Pipe JSON matching the hook's expected input format:

```bash
# Should block (exit 2) — bare python
echo '{"tool_input":{"command":"python foo.py"}}' | python3 .claude/hooks/pre_bash_check.py
echo $?  # 2

# Should allow (exit 0)
echo '{"tool_input":{"command":"uv run python foo.py"}}' | python3 .claude/hooks/pre_bash_check.py
echo $?  # 0

# Should block (exit 2) — rm on protected dir
echo '{"tool_input":{"command":"rm -rf workspace/notes"}}' | python3 .claude/hooks/pre_bash_check.py
echo $?  # 2
```

## Adding a new hook

1. Create a Python script in `.claude/hooks/` — read JSON from stdin, exit 0 or 2
2. Wire it in `.claude/settings.json` under the appropriate event
3. Document which rule from `.claude/rules/` it enforces (in the script's docstring)
4. Test it manually with piped JSON before relying on it

## Disabling hooks

- **One hook:** Remove or comment out its entry in `.claude/settings.json`
- **All hooks:** Add `"disableAllHooks": true` to `.claude/settings.json`
- **Per-user overrides:** Use `.claude/settings.local.json` (gitignored) to override specific hooks

## Viewing active hooks

Type `/hooks` in Claude Code to see all configured hooks grouped by event.
