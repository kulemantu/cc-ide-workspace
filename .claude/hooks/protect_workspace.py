"""Block destructive rm commands targeting protected directories.

Rule: workspace/CLAUDE.md — "Do not reorganize, rename, or move the user's files"
Rule: .claude/rules/sessions.md — .sessions/ and .local/ are never deleted
"""

from __future__ import annotations

import json
import re
import sys

PROTECTED = ["workspace/", ".sessions/", ".local/"]


def main() -> int:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    # Check if rm targets any protected directory
    if re.search(r"\brm\b", command):
        for directory in PROTECTED:
            if directory in command:
                print(
                    f"Blocked: destructive operation targeting {directory}. "
                    "These files must not be deleted without explicit user approval.",
                    file=sys.stderr,
                )
                return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
