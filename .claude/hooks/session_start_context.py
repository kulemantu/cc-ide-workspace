"""Inject three-layer continuity context on session startup.

Rule: .claude/rules/sessions.md — Three-Layer Continuity Model
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    # Consume stdin (required by hook protocol)
    sys.stdin.read()

    print(
        "Three-layer continuity: "
        "(1) git = what exists now, "
        "(2) .sessions/ = why it was built, what was tried, what is next, "
        "(3) .local/ = how to operate it (prompts, runbooks, credentials)."
    )

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    sessions_dir = Path(project_dir) / ".sessions"

    if sessions_dir.is_dir():
        session_files = sorted(sessions_dir.glob("SESSION-*.md"), reverse=True)
        if session_files:
            print(f"Most recent session: {session_files[0].name}")
        else:
            print("No session files found — consider creating one for this task.")
    else:
        print("No .sessions/ directory — it will be created when a session starts.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
