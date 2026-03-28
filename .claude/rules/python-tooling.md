---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
  - "**/requirements*.txt"
  - "**/setup.py"
  - "**/setup.cfg"
---

# Python Tooling

- Use `uv` to run Python commands: `uv run pytest`, not `python -m pytest`
- Use `ruff` for linting/formatting, not `black` or `flake8`
- Use `pyright` for type checking
