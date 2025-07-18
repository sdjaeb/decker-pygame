"""This module defines the application service for game settings."""

from decker_pygame.application.dtos import OptionsViewDTO
from decker_pygame.ports.service_interfaces import SettingsServiceInterface


class SettingsService(SettingsServiceInterface):
    """Application service for managing game settings.

    For now, this service holds the settings in memory. A future implementation
    could use a repository to persist these settings to a file.
    """

    def __init__(
        self, initial_sound_enabled: bool = True, initial_tooltips_enabled: bool = True
    ):
        self._sound_enabled = initial_sound_enabled
        self._tooltips_enabled = initial_tooltips_enabled

    def get_options(self) -> OptionsViewDTO:
        """Retrieves the current game options."""
        return OptionsViewDTO(
            sound_enabled=self._sound_enabled,
            tooltips_enabled=self._tooltips_enabled,
        )

    def set_sound_enabled(self, enabled: bool) -> None:
        """Sets the sound enabled state."""
        self._sound_enabled = enabled

    def set_tooltips_enabled(self, enabled: bool) -> None:
        """Sets the tooltips enabled state."""
        self._tooltips_enabled = enabled
