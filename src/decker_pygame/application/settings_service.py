"""This module defines the application service for game settings."""

from decker_pygame.application.dtos import OptionsViewDTO, SoundEditViewDTO
from decker_pygame.ports.service_interfaces import SettingsServiceInterface


class SettingsService(SettingsServiceInterface):
    """Application service for managing game settings.

    For now, this service holds the settings in memory. A future implementation
    could use a repository to persist these settings to a file.
    """

    def __init__(
        self,
        initial_sound_enabled: bool = True,
        initial_tooltips_enabled: bool = True,
        initial_master_volume: float = 1.0,
        initial_music_volume: float = 1.0,
        initial_sfx_volume: float = 1.0,
    ):
        self._sound_enabled = initial_sound_enabled
        self._tooltips_enabled = initial_tooltips_enabled
        self._master_volume = initial_master_volume
        self._music_volume = initial_music_volume
        self._sfx_volume = initial_sfx_volume

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

    def get_sound_options(self) -> SoundEditViewDTO:
        """Retrieves the current sound volume options."""
        return SoundEditViewDTO(
            master_volume=self._master_volume,
            music_volume=self._music_volume,
            sfx_volume=self._sfx_volume,
        )

    def set_master_volume(self, volume: float) -> None:
        """Sets the master volume level, clamping between 0.0 and 1.0."""
        self._master_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float) -> None:
        """Sets the music volume level, clamping between 0.0 and 1.0."""
        self._music_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float) -> None:
        """Sets the sound effects volume level, clamping between 0.0 and 1.0."""
        self._sfx_volume = max(0.0, min(1.0, volume))
