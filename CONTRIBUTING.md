# Contributing to IT Incident Copilot

Thank you for your interest in contributing! This document explains the process for making changes.

---

## Getting Started

1. Fork the repository and clone your fork
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies (including dev extras):

   ```bash
   pip install -e ".[dev]"
   ```

4. Copy `.env.example` to `.env` and fill in your API keys

---

## Development Workflow

### Running tests

```bash
make test
# or
pytest
```

### Linting

```bash
make lint
# or
ruff check .
ruff format --check .
```

### Type checking

```bash
make typecheck
# or
mypy src/
```

### All checks at once

```bash
make check
```

---

## Making Changes

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes following the existing code style
3. Add or update tests for your changes in `tests/`
4. Ensure all tests pass and linting is clean
5. Commit with a descriptive message
6. Open a pull request against `main`

---

## Code Style

- Python 3.11+
- Formatted with **ruff** (line length 100)
- Type hints required for all public functions
- Docstrings in Google style for all public classes and functions

---

## Reporting Issues

Please open a GitHub issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs. actual behaviour
- Python version and OS

---

## License

By contributing you agree that your changes will be licensed under the [MIT License](LICENSE).
