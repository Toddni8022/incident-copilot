"""Tests for configuration management."""

import pytest
from unittest.mock import patch

from incident_copilot.config import Config, setup_logging, DEFAULT_MODEL, DEFAULT_TEMPERATURE


class TestConfig:
    """Tests for the Config class."""

    def test_defaults(self, tmp_path):
        """Config initializes with expected defaults when env vars are absent."""
        with patch.dict(
            "os.environ",
            {"OUTPUT_DIR": str(tmp_path)},
            clear=False,
        ):
            # Remove optional keys so we get clean defaults
            with patch.dict("os.environ", {"OPENAI_API_KEY": "", "SLACK_BOT_TOKEN": ""}, clear=False):
                config = Config()
        assert config.model == DEFAULT_MODEL
        assert config.temperature == DEFAULT_TEMPERATURE

    def test_has_openai_true(self, mock_config):
        """has_openai returns True when OPENAI_API_KEY is set."""
        assert mock_config.has_openai() is True

    def test_has_openai_false(self, tmp_path):
        """has_openai returns False when OPENAI_API_KEY is absent."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "", "OUTPUT_DIR": str(tmp_path)}):
            config = Config()
        assert config.has_openai() is False

    def test_has_slack_true(self, mock_config):
        """has_slack returns True when SLACK_BOT_TOKEN is set."""
        assert mock_config.has_slack() is True

    def test_has_slack_false(self, tmp_path):
        """has_slack returns False when SLACK_BOT_TOKEN is absent."""
        with patch.dict("os.environ", {"SLACK_BOT_TOKEN": "", "OUTPUT_DIR": str(tmp_path)}):
            config = Config()
        assert config.has_slack() is False

    def test_validate_openai_raises_when_missing(self, tmp_path):
        """validate_openai raises ValueError when API key is not set."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "", "OUTPUT_DIR": str(tmp_path)}):
            config = Config()
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            config.validate_openai()

    def test_validate_slack_raises_when_missing(self, tmp_path):
        """validate_slack raises ValueError when bot token is not set."""
        with patch.dict("os.environ", {"SLACK_BOT_TOKEN": "", "OUTPUT_DIR": str(tmp_path)}):
            config = Config()
        with pytest.raises(ValueError, match="SLACK_BOT_TOKEN"):
            config.validate_slack()

    def test_validate_openai_passes(self, mock_config):
        """validate_openai does not raise when API key is set."""
        mock_config.validate_openai()  # should not raise

    def test_validate_slack_passes(self, mock_config):
        """validate_slack does not raise when bot token is set."""
        mock_config.validate_slack()  # should not raise

    def test_output_dir_created(self, tmp_path):
        """Config creates the output directory if it does not exist."""
        new_dir = tmp_path / "new_output"
        assert not new_dir.exists()
        with patch.dict("os.environ", {"OUTPUT_DIR": str(new_dir)}):
            Config()
        assert new_dir.exists()


class TestSetupLogging:
    """Tests for setup_logging helper."""

    def test_returns_logger(self):
        """setup_logging returns a Logger with the given name."""
        import logging

        logger = setup_logging("test_logger")
        assert logger.name == "test_logger"
        assert isinstance(logger, logging.Logger)
