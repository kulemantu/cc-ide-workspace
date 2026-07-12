"""Template smoke test: keeps `uv run pytest` green on a fresh clone.

An empty tests/ makes pytest exit 5 ("no tests collected"), which fails the
fresh-clone command advertised in CLAUDE.md. This test also pins the invariant
that makes that command work at all: the scripts env is a virtual (non-package)
uv project, so `uv sync` never tries to build/install it. Replace with real
tests as scripts/src/ gains modules.
"""

import tomllib
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent


def test_scripts_env_is_wired_for_fresh_clone() -> None:
    pyproject = tomllib.loads((SCRIPTS / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject.get("tool", {}).get("uv", {}).get("package") is False, (
        "scripts/ is a virtual uv env; packaging it breaks fresh-clone uv sync"
    )
    assert (SCRIPTS / "src").is_dir(), "CLAUDE.md advertises modules in scripts/src/"
