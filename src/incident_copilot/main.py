"""Command-line interface for IT Incident Copilot."""

from datetime import datetime
from pathlib import Path
import sys
import logging
from openai import APIError, APIConnectionError, RateLimitError
from pydantic import ValidationError

from incident_copilot.config import Config, setup_logging, TIMESTAMP_FORMAT
from incident_copilot.parser.incident_parser import IncidentCopilot
from incident_copilot.utils import save_report

# Setup logging
logger = setup_logging(__name__)


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
        config = Config()
        copilot = IncidentCopilot(config)

        raw_input = read_input()

        if not raw_input.strip():
            logger.error("No input provided")
            print("Error: No input provided. Please provide incident notes to analyze.")
            return 1

        print("\n🔄 Analyzing incident...\n")

        report = copilot.parse_incident(raw_input)
        markdown = copilot.format_markdown(report)
        output_file = save_report(markdown, config.output_dir)

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
        print("Error: Unable to connect to OpenAI API. Please check your internet connection.")
        return 1

    except RateLimitError as e:
        logger.error("Rate limit exceeded: %s", e)
        print("Error: OpenAI rate limit exceeded. Please try again later.")
        return 1

    except APIError as e:
        logger.error("OpenAI API error: %s", e)
        print(f"Error: OpenAI API error - {e}")
        return 1

    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print("Error: Received invalid response from OpenAI. Please try again.")
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
