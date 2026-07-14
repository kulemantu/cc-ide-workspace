import subprocess
from pathlib import Path

from src.workspace_check import findings_block, inspect_path, inspect_text

ROOT = Path(__file__).resolve().parents[2]


def test_private_capture_paths_block_tracking() -> None:
    findings = inspect_path("workspace/client/screenshots/raw-dashboard.png")
    assert any(finding.severity == "BLOCK" for finding in findings)


def test_private_capture_paths_block_mixed_case_tracking() -> None:
    findings = inspect_path("workspace/client/Screenshots/raw-dashboard.png")
    assert any(finding.severity == "BLOCK" for finding in findings)


def test_media_outside_capture_paths_requires_manual_review() -> None:
    findings = inspect_path("docs/sanitized-workflow.png")
    assert [finding.severity for finding in findings] == ["WARN"]
    assert findings_block(findings, allow_reviewed_media=False)
    assert not findings_block(findings, allow_reviewed_media=True)


def test_env_example_is_allowed() -> None:
    assert inspect_path("apps/example/.env.example") == []


def test_high_confidence_secret_content_blocks_sharing() -> None:
    fake_token = "ghp_" + "A" * 24
    findings = inspect_text("notes.md", f"token={fake_token}")
    assert findings[0].severity == "BLOCK"
    assert "GitHub token" in findings[0].message


def test_sensitive_capture_paths_are_gitignored() -> None:
    paths = [
        "screenshots/raw.png",
        "workspace/client/scratchpad/notes.md",
        ".playwright-mcp/page.png",
        "playwright-report/index.html",
        "test-results/trace.zip",
    ]
    for path in paths:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", path],
            cwd=ROOT,
            check=False,
        )
        assert result.returncode == 0, f"expected {path} to be ignored"
