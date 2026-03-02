.PHONY: setup test lint format typecheck check run docker-build docker-up clean help

## Display this help message
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## Install the package and all dev dependencies
setup:
	pip install -e ".[dev]"

## Run the pytest test suite
test:
	pytest --cov=incident_copilot --cov-report=term-missing

## Run ruff linter
lint:
	ruff check .

## Auto-fix lint issues and reformat code
format:
	ruff check --fix .
	ruff format .

## Run mypy type checking
typecheck:
	mypy src/

## Run lint + typecheck + tests
check: lint typecheck test

## Start the Streamlit web UI
run:
	streamlit run app.py

## Build the Docker image
docker-build:
	docker build -t incident-copilot .

## Start the application with Docker Compose
docker-up:
	docker compose up

## Remove Python cache files and build artefacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage htmlcov/ dist/ build/ *.egg-info/
