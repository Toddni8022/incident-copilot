"""Utility functions for IT Incident Copilot."""

from datetime import datetime
from pathlib import Path
from typing import List, Dict
import logging

from incident_copilot.config import TIMESTAMP_FORMAT, setup_logging

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
    output_path.write_text(markdown, encoding="utf-8")
    logger.info("Report saved to: %s", output_path)
    return str(output_path)


def combine_messages(messages: List[Dict]) -> str:
    """Combine a list of message dicts into a single text string.

    Args:
        messages: List of message dictionaries with a ``text`` key.

    Returns:
        str: Combined message text joined by newlines.
    """
    return "\n".join([msg.get("text", "") for msg in messages if "text" in msg])
