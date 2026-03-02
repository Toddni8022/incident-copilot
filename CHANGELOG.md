# Changelog

All notable changes to IT Incident Copilot are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- `src/incident_copilot/` installable package with sub-packages for parsing and integrations
- `tests/` directory with pytest test suite covering config, parser, Slack integration, and utilities
- `data/` directory with example incident tickets
- `docs/` directory: setup guide, Slack setup, parsing docs, architecture, API reference
- `LICENSE` (MIT)
- `CONTRIBUTING.md`
- `pyproject.toml` with project metadata, ruff, mypy, and pytest configuration
- `setup.py` for legacy editable installs
- `.github/workflows/ci.yml` — CI pipeline (lint, type-check, test)
- `Dockerfile` and `docker-compose.yml` for containerised deployment
- `.env.example` with documented environment variables
- `.dockerignore`
- `.editorconfig`
- `pytest.ini`
- `.coveragerc`
- `Makefile` with common development targets
- Comprehensive `.gitignore`
- Pinned versions in `requirements.txt`

### Changed
- Moved Pydantic data models to `src/incident_copilot/models.py`
- Extracted shared utilities (`save_report`, `combine_messages`) to `src/incident_copilot/utils.py`
- Wrapped Slack SDK in `SlackIntegration` class in `src/incident_copilot/integrations/slack.py`
- Updated `README.md` with badges, architecture diagram, and full usage guide

---

## [0.1.0] — 2024-01-01

### Added
- Initial release
- Streamlit web dashboard (`app.py`)
- CLI entry point (`main.py`)
- Manual Slack analysis script (`slack_manual.py`)
- OpenAI GPT-4 structured output parsing (`incident_parser.py`)
- Environment-based configuration (`config.py`)
- Pydantic data models
