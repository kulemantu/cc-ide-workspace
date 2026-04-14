"""Block bare python/python3 invocations — must use 'uv run python'.

Rule: .claude/rules/python-tooling.md
"""

from __future__ import annotations

import json
import re
import sys


def main() -> int:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    # Match bare python/python3 at start or after shell operators (&&, ;, |)
    # but not when preceded by "uv run"
    if re.search(r"(?:^|&&|;|\|)\s*python3?\s", command) and not re.search(
        r"uv\s+run\s+python", command
    ):
        print(
            'Use "uv run python" instead of bare "python". '
            "All Python in this repo runs through uv.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
