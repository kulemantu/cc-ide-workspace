"""Inject session-update reminder before context compaction.

Rule: .claude/rules/sessions.md — "Before context compaction: always update
the session file with current progress, pending work, and any decisions or
context that would be lost."
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    # Consume stdin (required by hook protocol)
    sys.stdin.read()

    print(
        "COMPACTION IMMINENT — Update the .sessions/ file with current progress, "
        "pending work, and key decisions before context is lost. "
        "The session file is the recovery point after compaction."
    )

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    sessions_dir = Path(project_dir) / ".sessions"

    if sessions_dir.is_dir():
        session_files = sorted(sessions_dir.glob("SESSION-*.md"), reverse=True)
        if session_files:
            print(f"Most recent session: {session_files[0].name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
