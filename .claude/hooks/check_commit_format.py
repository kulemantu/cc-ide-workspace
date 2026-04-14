"""Validate conventional commit format: type(scope): description.

Rule: .claude/rules/git-conventions.md
Does NOT validate trailers (sign-off, co-author) — those are user-specific.
"""

from __future__ import annotations

import json
import re
import sys

VALID_TYPES = [
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

COMMIT_RE = re.compile(
    r"^(" + "|".join(VALID_TYPES) + r")(\([^)]+\))?: .+"
)


def extract_message(command: str) -> str | None:
    """Extract the commit message from a git commit command string."""
    # Match -m "message" or -m 'message'
    match = re.search(r'-m\s+["\'](.+?)["\']', command)
    if match:
        return match.group(1)

    # Match heredoc pattern: -m "$(cat <<'EOF'\nmessage\n..."
    match = re.search(r"-m\s+\"\$\(cat\s+<<", command)
    if match:
        # For heredoc, extract the first line after the heredoc marker
        lines = command.split("\n")
        for i, line in enumerate(lines):
            if "EOF" in line and i == 0:
                continue
            stripped = line.strip()
            if stripped and stripped != "EOF" and "cat <<" not in stripped:
                return stripped

    return None


def main() -> int:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    # Only validate if we can extract a message
    message = extract_message(command)
    if message is None:
        return 0

    first_line = message.split("\n")[0].strip()

    if not COMMIT_RE.match(first_line):
        types_str = ", ".join(VALID_TYPES)
        print(
            f"Commit message must follow conventional format: type(scope): description\n"
            f"Valid types: {types_str}\n"
            f"Got: {first_line}",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
