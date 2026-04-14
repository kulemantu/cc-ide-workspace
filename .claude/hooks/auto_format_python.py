"""Auto-format Python files with ruff after edits.

Rule: .claude/rules/python-tooling.md — ruff is the standard formatter.
Runs as PostToolUse on Edit|Write. Never blocks (always exits 0).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys


def main() -> int:
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith(".py"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    scripts_dir = os.path.join(project_dir, "scripts") if project_dir else "scripts"

    try:
        subprocess.run(
            ["uv", "run", "ruff", "format", file_path],
            cwd=scripts_dir,
            capture_output=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass  # Formatting is best-effort, never blocks

    return 0


if __name__ == "__main__":
    sys.exit(main())
