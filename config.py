"""Configuration management for IT Incident Copilot."""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
DEFAULT_MODEL = "gpt-4o-2024-08-06"
OUTPUT_DIR = "output"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MESSAGE_LIMIT = 50
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class Config:
    """Application configuration with validation."""

    def __init__(self):
        """Initialize configuration and validate required environment variables."""
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.slack_bot_token: Optional[str] = os.getenv("SLACK_BOT_TOKEN")
        self.model: str = os.getenv("MODEL", DEFAULT_MODEL)
        self.output_dir: str = os.getenv("OUTPUT_DIR", OUTPUT_DIR)
        self.temperature: float = float(os.getenv("TEMPERATURE", str(DEFAULT_TEMPERATURE)))

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def validate_openai(self) -> None:
        """Validate OpenAI API key is set.

        Raises:
            ValueError: If OPENAI_API_KEY is not set.
        """
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )

    def validate_slack(self) -> None:
        """Validate Slack bot token is set.

        Raises:
            ValueError: If SLACK_BOT_TOKEN is not set.
        """
        if not self.slack_bot_token:
            raise ValueError(
                "SLACK_BOT_TOKEN environment variable is required for Slack integration. "
                "Please set it in your .env file or environment."
            )

    def has_slack(self) -> bool:
        """Check if Slack configuration is available.

        Returns:
            bool: True if Slack bot token is configured.
        """
        return bool(self.slack_bot_token)

    def has_openai(self) -> bool:
        """Check if OpenAI configuration is available.

        Returns:
            bool: True if OpenAI API key is configured.
        """
        return bool(self.openai_api_key)


def setup_logging(name: str = __name__) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        name: Logger name (typically __name__ of the module).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
        ]
    )
    return logging.getLogger(name)
