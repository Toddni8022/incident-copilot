# Data Directory

This directory contains sample and example data for IT Incident Copilot.

## Structure

```
data/
└── examples/
    └── sample_ticket.txt   — Example incident ticket for testing
```

## Usage

Use the files in `examples/` to test the application without connecting to a live Slack workspace or OpenAI API.

### Running with sample data (CLI)

```bash
python main.py data/examples/sample_ticket.txt
```

### Running with sample data (package entry point)

```bash
incident-copilot data/examples/sample_ticket.txt
```
