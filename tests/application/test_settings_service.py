"""Tests for the SettingsService."""

import pytest

from decker_pygame.application.settings_service import SettingsService


@pytest.fixture
def settings_service() -> SettingsService:
    """Provides a SettingsService instance with default values."""
    return SettingsService()


def test_settings_service_initial_state(settings_service: SettingsService):
    """Tests that the service initializes with the correct default options."""
    options = settings_service.get_options()
    assert options.sound_enabled is True
    assert options.tooltips_enabled is True


def test_set_sound_enabled(settings_service: SettingsService):
    """Tests toggling the sound setting."""
    # Initial state is True
    assert settings_service.get_options().sound_enabled is True

    # Set to False
    settings_service.set_sound_enabled(False)
    assert settings_service.get_options().sound_enabled is False

    # Set back to True
    settings_service.set_sound_enabled(True)
    assert settings_service.get_options().sound_enabled is True


def test_set_tooltips_enabled(settings_service: SettingsService):
    """Tests toggling the tooltips setting."""
    # Initial state is True
    assert settings_service.get_options().tooltips_enabled is True

    # Set to False
    settings_service.set_tooltips_enabled(False)
    assert settings_service.get_options().tooltips_enabled is False

    # Set back to True
    settings_service.set_tooltips_enabled(True)
    assert settings_service.get_options().tooltips_enabled is True
