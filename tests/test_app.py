"""Tests for Streamlit app utility functions."""

import pytest
from pathlib import Path
from unittest.mock import patch

from incident_copilot.utils import save_report, combine_messages


class TestSaveReport:
    """Tests for the save_report utility."""

    def test_saves_file(self, tmp_path):
        """save_report writes the markdown content to a file."""
        content = "# Test Report"
        path = save_report(content, str(tmp_path))
        assert Path(path).exists()
        assert Path(path).read_text(encoding="utf-8") == content

    def test_filename_contains_timestamp(self, tmp_path):
        """save_report uses a timestamped filename."""
        path = save_report("# Report", str(tmp_path))
        assert Path(path).name.startswith("incident_report_")
        assert Path(path).suffix == ".md"

    def test_returns_path_string(self, tmp_path):
        """save_report returns a string path."""
        result = save_report("# Report", str(tmp_path))
        assert isinstance(result, str)
