# scripts/

This is the Python environment. All scripts, modules, and tests live here.

## Commands

All commands run from the `scripts/` directory:

```bash
cd scripts
uv run pytest                              # Run all tests
uv run pytest tests/test_foo.py::test_bar  # Run a single test
uv run ruff check .                        # Lint
uv run ruff format .                       # Format
uv run pyright                             # Type check
uv run python src/new_project/my_script.py # Run a script
```

Always use `uv run` — never bare `python`.

**Environment management**: run `uv sync` when dependencies change or the `.venv` is missing. Run `uv add <package>` to add new dependencies. These are Claude-managed — the user does not need to run them.

## Conventions

- **Python over bash**: always write scripts in Python, not bash. Python scripts are testable, readable, and run in the managed environment.
- **Always write tests**: every module in `src/` should have a corresponding test in `tests/`.
- **Output files**: all generated output goes to `workspace/outputs/`, not here.
- **Input files**: read user files from `workspace/` or `.local/`.
- **Dependencies**: add with `uv add <package>` from this directory.
- **One-off scratch scripts**: put in `.local/` at the project root, not here. `src/` is for reusable code.

## Structure

- `src/new_project/` — installable package. Claude adds modules here as the project needs them.
- `tests/` — tests for `src/` modules.
- `pyproject.toml` — dependencies and tool config (ruff, pyright, pytest).
- `.venv/` — managed by uv, gitignored.
