"""Unified pre-Bash checks — single hook instead of four separate evaluations.

Consolidates: enforce_uv_run, protect_workspace, check_commit_format, require_push_approval.

Rules enforced:
  - .claude/rules/python-tooling.md (bare python blocked)
  - .claude/rules/sessions.md (workspace/sessions/local protected)
  - .claude/rules/git-conventions.md (commit format, push approval)
"""

from __future__ import annotations

import json
import re
import sys

VALID_COMMIT_TYPES = [
    "feat",
    "fix",
    "docs",
    "chore",
    "refactor",
    "test",
    "style",
    "ci",
    "perf",
    "build",
]
COMMIT_RE = re.compile(r"^(" + "|".join(VALID_COMMIT_TYPES) + r")(\([^)]+\))?: .+")
PROTECTED_DIRS = ["workspace/", ".sessions/", ".local/"]


def extract_commit_message(command: str) -> str | None:
    """Extract the commit message from a git commit command string."""
    # Heredoc pattern first — must check before simple quotes since heredocs
    # contain quotes that the simple regex would incorrectly match
    match = re.search(r"-m\s+\"\$\(cat\s+<<", command)
    if match:
        lines = command.split("\n")
        for i, line in enumerate(lines):
            if "EOF" in line and i == 0:
                continue
            stripped = line.strip()
            if stripped and stripped != "EOF" and "cat <<" not in stripped:
                return stripped
        return None

    # Simple -m "message" or -m 'message'
    match = re.search(r'-m\s+["\'](.+?)["\']', command)
    if match:
        return match.group(1)

    return None


def check_uv_run(command: str) -> str | None:
    """Block bare python/python3 — must use 'uv run python'."""
    if re.search(r"(?:^|&&|;|\|)\s*python3?\s", command) and not re.search(
        r"uv\s+run\s+python", command
    ):
        return (
            'Use "uv run python" instead of bare "python". '
            "All Python in this repo runs through uv."
        )
    return None


def check_protected_dirs(command: str) -> str | None:
    """Block rm on workspace/, .sessions/, .local/."""
    if re.search(r"\brm\b", command):
        for d in PROTECTED_DIRS:
            # Match as standalone path — not as substring of a parent dir name
            # e.g., "workspace/" but not "cc-ide-workspace/"
            if re.search(r"(?<![a-zA-Z0-9_-])" + re.escape(d), command):
                return (
                    f"Blocked: destructive operation targeting {d}. "
                    "These files must not be deleted without explicit user approval."
                )
    return None


def check_commit_format(command: str) -> str | None:
    """Validate conventional commit format: type(scope): description."""
    if not re.search(r"\bgit\s+commit\b", command):
        return None
    message = extract_commit_message(command)
    if message is None:
        return None
    first_line = message.split("\n")[0].strip()
    if not COMMIT_RE.match(first_line):
        types_str = ", ".join(VALID_COMMIT_TYPES)
        return (
            f"Commit message must follow conventional format: type(scope): description\n"
            f"Valid types: {types_str}\n"
            f"Got: {first_line}"
        )
    return None


def check_push_approval(command: str) -> dict | None:
    """Force interactive approval for git push."""
    if re.search(r"\bgit\s+push\b", command):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": (
                    "Git push requires explicit user approval per project conventions."
                ),
            }
        }
    return None


def main() -> int:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    # Blocking checks (exit 2 to reject the tool call)
    for check in [check_uv_run, check_protected_dirs, check_commit_format]:
        error = check(command)
        if error:
            print(error, file=sys.stderr)
            return 2

    # Approval check (output JSON decision, exit 0)
    approval = check_push_approval(command)
    if approval:
        json.dump(approval, sys.stdout)

    return 0


if __name__ == "__main__":
    sys.exit(main())
