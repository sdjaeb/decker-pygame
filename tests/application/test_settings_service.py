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

    sound_options = settings_service.get_sound_options()
    assert sound_options.master_volume == 1.0
    assert sound_options.music_volume == 1.0
    assert sound_options.sfx_volume == 1.0


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


@pytest.mark.parametrize(
    "setter_name, getter_attr",
    [
        ("set_master_volume", "master_volume"),
        ("set_music_volume", "music_volume"),
        ("set_sfx_volume", "sfx_volume"),
    ],
)
def test_set_volume_levels(
    settings_service: SettingsService, setter_name: str, getter_attr: str
):
    """Tests setting various volume levels, including clamping."""
    setter_method = getattr(settings_service, setter_name)

    # Test setting a valid value
    setter_method(0.5)
    assert getattr(settings_service.get_sound_options(), getter_attr) == 0.5

    # Test clamping above 1.0
    setter_method(1.5)
    assert getattr(settings_service.get_sound_options(), getter_attr) == 1.0

    # Test clamping below 0.0
    setter_method(-0.5)
    assert getattr(settings_service.get_sound_options(), getter_attr) == 0.0
