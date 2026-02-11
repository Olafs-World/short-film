"""Tests for CLI interface."""

import pytest
from typer.testing import CliRunner

from short_film.cli import app

runner = CliRunner()


def test_cli_version():
    """Test version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "short-film version" in result.stdout


def test_cli_styles():
    """Test styles command."""
    result = runner.invoke(app, ["styles"])
    assert result.exit_code == 0
    assert "cinematic" in result.stdout.lower()
    assert "anime" in result.stdout.lower()


def test_cli_vibes():
    """Test vibes command."""
    result = runner.invoke(app, ["vibes"])
    assert result.exit_code == 0
    assert "epic" in result.stdout.lower()
    assert "suspenseful" in result.stdout.lower()


def test_cli_generate_missing_premise():
    """Test generate command without premise in non-interactive mode."""
    result = runner.invoke(
        app,
        ["generate", "--no-interactive"],
    )
    assert result.exit_code == 1
    assert "required" in result.stdout.lower()


@pytest.mark.integration
def test_cli_generate_full_integration(tmp_path):
    """Integration test for full generation flow."""
    # This would require real API keys and is expensive
    pytest.skip("Integration test - requires API keys and costs money")
