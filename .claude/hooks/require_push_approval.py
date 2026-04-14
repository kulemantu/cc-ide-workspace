"""Force interactive approval prompt for all git push commands.

Rule: .claude/rules/git-conventions.md — "Do NOT auto-push."
"""

from __future__ import annotations

import json
import sys


def main() -> int:
    # Consume stdin (required by hook protocol)
    sys.stdin.read()

    # Output decision JSON to force the permission prompt
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                "Git push requires explicit user approval per project conventions."
            ),
        }
    }
    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
