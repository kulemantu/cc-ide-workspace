#!/usr/bin/env python3
"""Check workspace confidentiality hygiene and run the local verification gate."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Literal

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
APP = ROOT / "apps" / "transcriber-prioritizer"

PRIVATE_PARTS = frozenset(
    {
        ".local",
        ".sessions",
        ".playwright-mcp",
        "scratchpad",
        "screenshots",
        "playwright-report",
        "test-results",
    }
)
SECRET_SUFFIXES = frozenset({".key", ".pem", ".p12", ".pfx"})
MEDIA_SUFFIXES = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".docx", ".pptx", ".mov", ".mp4"}
)
SECRET_NAMES = (
    re.compile(r"^client_secret.*\.json$", re.IGNORECASE),
    re.compile(r"^(?:credentials|token|service[-_]?account).*\.json$", re.IGNORECASE),
)
SECRET_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
)
MAX_TEXT_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True)
class Finding:
    severity: Literal["BLOCK", "WARN"]
    path: str
    message: str


def inspect_path(path: str) -> list[Finding]:
    """Return deterministic path/media findings without reading file content."""
    parsed = PurePosixPath(path)
    parts = set(parsed.parts)
    name = parsed.name
    lower_name = name.lower()
    findings: list[Finding] = []

    private_parts = sorted(parts & PRIVATE_PARTS)
    if private_parts:
        findings.append(
            Finding(
                "BLOCK",
                path,
                f"private capture path contains '{private_parts[0]}'; "
                "keep it untracked",
            )
        )

    is_env_example = lower_name.endswith(".env.example") or lower_name == ".env.example"
    is_env_file = (
        lower_name == ".env"
        or lower_name.startswith(".env.")
        or lower_name.endswith(".env")
    )
    if is_env_file and not is_env_example:
        findings.append(
            Finding("BLOCK", path, "environment file may contain credentials")
        )

    if parsed.suffix.lower() in SECRET_SUFFIXES or any(
        pattern.match(name) for pattern in SECRET_NAMES
    ):
        findings.append(
            Finding("BLOCK", path, "credential-shaped filename must not be tracked")
        )

    if parsed.suffix.lower() in MEDIA_SUFFIXES:
        findings.append(
            Finding(
                "WARN",
                path,
                "binary/media file requires manual review for visible data and "
                "metadata before sharing",
            )
        )

    return findings


def inspect_text(path: str, text: str) -> list[Finding]:
    """Detect only high-confidence secret shapes to keep false positives low."""
    return [
        Finding("BLOCK", path, f"high-confidence {label} pattern found")
        for label, pattern in SECRET_PATTERNS
        if pattern.search(text)
    ]


def git_paths(staged: bool) -> list[str]:
    command = (
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]
        if staged
        else ["git", "ls-files", "-z"]
    )
    result = subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
    return sorted(path for path in result.stdout.decode().split("\0") if path)


def inspect_files(paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for relative in paths:
        findings.extend(inspect_path(relative))
        absolute = ROOT / relative
        if not absolute.is_file() or absolute.stat().st_size > MAX_TEXT_BYTES:
            continue
        data = absolute.read_bytes()
        if b"\0" in data:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(inspect_text(relative, text))
    return sorted(
        findings, key=lambda item: (item.severity != "BLOCK", item.path, item.message)
    )


def print_findings(findings: list[Finding], as_json: bool) -> None:
    if as_json:
        import json

        print(json.dumps([asdict(finding) for finding in findings], indent=2))
        return
    for finding in findings:
        print(f"[{finding.severity}] {finding.path}: {finding.message}")


def findings_block(findings: list[Finding], allow_reviewed_media: bool) -> bool:
    return any(finding.severity == "BLOCK" for finding in findings) or (
        not allow_reviewed_media
        and any(finding.severity == "WARN" for finding in findings)
    )


def run_hygiene(
    staged: bool,
    as_json: bool = False,
    allow_reviewed_media: bool = False,
) -> int:
    paths = git_paths(staged)
    findings = inspect_files(paths)
    print_findings(findings, as_json)
    blockers = sum(finding.severity == "BLOCK" for finding in findings)
    warnings = sum(finding.severity == "WARN" for finding in findings)
    if not as_json:
        scope = "staged" if staged else "tracked"
        print(
            f"[SUMMARY] {len(paths)} {scope} files; {blockers} blocker(s); "
            f"{warnings} warning(s)"
        )
        if warnings and not allow_reviewed_media:
            print(
                "[ACTION] Review every media warning, then rerun with "
                "--allow-reviewed-media"
            )
    return 1 if findings_block(findings, allow_reviewed_media) else 0


def run_command(command: list[str], cwd: Path) -> int:
    shown = " ".join(command)
    print(f"\n[RUN] ({cwd.relative_to(ROOT) or '.'}) {shown}", flush=True)
    return subprocess.run(command, cwd=cwd, check=False).returncode


def run_verify(allow_reviewed_media: bool = False) -> int:
    if run_hygiene(staged=False, allow_reviewed_media=allow_reviewed_media):
        return 1
    commands = (
        (["git", "diff", "--check"], ROOT),
        (["git", "diff", "--cached", "--check"], ROOT),
        (["uv", "run", "pytest", "-q"], SCRIPTS),
        (["uv", "run", "ruff", "check", "."], SCRIPTS),
        (["uv", "run", "pyright"], SCRIPTS),
        (["uv", "run", "python3", "-m", "unittest", "test_transcribe_call", "-v"], APP),
    )
    for command, cwd in commands:
        if code := run_command(command, cwd):
            return code
    print("\n[SUCCESS] hygiene and verification checks passed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check confidentiality hygiene or run the complete workspace "
            "verification gate."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    hygiene = subparsers.add_parser(
        "hygiene", help="scan tracked or staged files for sharing risks"
    )
    hygiene.add_argument(
        "--staged", action="store_true", help="scan only staged additions and changes"
    )
    hygiene.add_argument("--json", action="store_true", help="emit findings as JSON")
    hygiene.add_argument(
        "--allow-reviewed-media",
        action="store_true",
        help="confirm that every WARN media file was manually reviewed",
    )

    verify = subparsers.add_parser(
        "verify", help="run hygiene, diff, tests, lint, and type checks"
    )
    verify.add_argument(
        "--allow-reviewed-media",
        action="store_true",
        help="confirm that every WARN media file was manually reviewed",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "hygiene":
        return run_hygiene(
            staged=args.staged,
            as_json=args.json,
            allow_reviewed_media=args.allow_reviewed_media,
        )
    return run_verify(allow_reviewed_media=args.allow_reviewed_media)


if __name__ == "__main__":
    sys.exit(main())
