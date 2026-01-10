"""Command-line interface for IT Incident Copilot."""

from incident_parser import IncidentCopilot
from datetime import datetime
from pathlib import Path
import sys
import logging
from typing import Optional
from anthropic import APIError, APIConnectionError, RateLimitError
from pydantic import ValidationError
from config import Config, setup_logging, TIMESTAMP_FORMAT

# Setup logging
logger = setup_logging(__name__)


def save_report(markdown: str, output_dir: str) -> str:
    """Save incident report to a timestamped file.

    Args:
        markdown: Markdown-formatted report content.
        output_dir: Directory to save the report in.

    Returns:
        str: Path to the saved file.

    Raises:
        OSError: If unable to write to the file.
    """
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    output_path = Path(output_dir) / f"incident_report_{timestamp}.md"

    try:
        output_path.write_text(markdown, encoding="utf-8")
        logger.info("Report saved to: %s", output_path)
        return str(output_path)
    except OSError as e:
        logger.error("Failed to save report to %s: %s", output_path, e)
        raise


def read_input() -> str:
    """Read incident input from file or stdin.

    Returns:
        str: Raw incident input text.

    Raises:
        FileNotFoundError: If input file doesn't exist.
        OSError: If unable to read input file.
    """
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        logger.info("Reading input from file: %s", input_file)
        return input_file.read_text(encoding="utf-8")
    else:
        print("Enter incident notes (press Ctrl+D on Unix/Ctrl+Z then Enter on Windows when done):")
        logger.info("Reading input from stdin")
        return sys.stdin.read()


def main() -> int:
    """Main entry point for CLI.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    try:
        # Initialize configuration and copilot
        config = Config()
        copilot = IncidentCopilot(config)

        # Read input
        raw_input = read_input()

        if not raw_input.strip():
            logger.error("No input provided")
            print("Error: No input provided. Please provide incident notes to analyze.")
            return 1

        print("\n🔄 Analyzing incident...\n")

        # Parse incident
        report = copilot.parse_incident(raw_input)

        # Generate markdown
        markdown = copilot.format_markdown(report)

        # Save output
        output_file = save_report(markdown, config.output_dir)

        # Display results
        print(markdown)
        print(f"\n✅ Report saved to: {output_file}")

        return 0

    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        print(f"Error: {e}")
        return 1

    except ValueError as e:
        logger.error("Invalid input: %s", e)
        print(f"Error: {e}")
        return 1

    except APIConnectionError as e:
        logger.error("API connection failed: %s", e)
        print(f"Error: Unable to connect to Claude API. Please check your internet connection.")
        return 1

    except RateLimitError as e:
        logger.error("Rate limit exceeded: %s", e)
        print(f"Error: Claude API rate limit exceeded. Please try again later.")
        return 1

    except APIError as e:
        logger.error("Claude API error: %s", e)
        print(f"Error: Claude API error - {e}")
        return 1

    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print(f"Error: Received invalid response from Claude. Please try again.")
        return 1

    except OSError as e:
        logger.error("File system error: %s", e)
        print(f"Error: Unable to read/write files - {e}")
        return 1

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n\nOperation cancelled.")
        return 1

    except Exception as e:
        logger.exception("Unexpected error occurred: %s", e)
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
