---
paths:
  - "scripts/**/*.py"
  - "scripts/pyproject.toml"
---

# Python Tooling

- All Python code lives in `scripts/`. Run commands from there: `cd scripts && uv run ...`
- Use `uv` to run Python commands: `uv run pytest`, not `python -m pytest`
- Use `ruff` for linting/formatting, not `black` or `flake8`
- Use `pyright` for type checking
- **Always write scripts in Python, not bash.** Python scripts are testable, readable, and run in the managed environment.
- **Always write tests.** Every module in `scripts/src/` should have a corresponding test in `scripts/tests/`.
- Script outputs go to `workspace/.outputs/**/*`. Input files come from `workspace/` or `.local/`.
- One-off scratch scripts go in `.local/`, not `scripts/src/`. The `src/` directory is for reusable code.