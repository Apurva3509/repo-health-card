# Contributing

Contributions should begin with a focused issue describing the user-facing
problem. Keep pull requests small enough to review independently, include tests
for behavioral changes, and explain any compatibility implications.

## Local setup

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests
```

