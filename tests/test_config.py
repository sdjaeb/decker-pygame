import importlib
from pathlib import Path


def test_default_settings(monkeypatch):
    """Test that settings load with default values when no overrides are present."""
    # Ensure no conflicting environment variables are set for the values we are testing.
    monkeypatch.delenv("SCREEN_WIDTH", raising=False)
    monkeypatch.delenv("SCREEN_HEIGHT", raising=False)
    monkeypatch.delenv("FULLSCREEN", raising=False)

    # We must reload the config module to re-trigger the Settings instantiation.
    from decker_pygame import config

    importlib.reload(config)

    assert config.settings.screen_width == 1280
    assert config.settings.screen_height == 720
    assert config.settings.fullscreen is False


def test_settings_from_env_file(tmp_path: Path, monkeypatch):
    """Test that settings can be loaded from a .env file."""
    env_file = tmp_path / ".env"
    env_file.write_text("SCREEN_WIDTH=1024\nFULLSCREEN=true")

    # Change to the temp directory so pydantic-settings finds the .env file.
    monkeypatch.chdir(tmp_path)
    # Ensure no conflicting environment variables are set.
    monkeypatch.delenv("SCREEN_WIDTH", raising=False)
    monkeypatch.delenv("FULLSCREEN", raising=False)

    from decker_pygame import config

    importlib.reload(config)

    assert config.settings.screen_width == 1024
    assert config.settings.screen_height == 720  # Should remain default.
    assert config.settings.fullscreen is True


def test_settings_from_environment_variables(monkeypatch):
    """Test that environment variables override default values."""
    monkeypatch.setenv("SCREEN_WIDTH", "800")
    monkeypatch.setenv("FULLSCREEN", "1")

    from decker_pygame import config

    importlib.reload(config)

    assert config.settings.screen_width == 800
    assert config.settings.fullscreen is True
