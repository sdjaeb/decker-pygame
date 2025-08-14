"""This module contains actions used for debugging purposes."""

import uuid
from typing import TYPE_CHECKING

from decker_pygame.domain.ids import DSFileId

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class DebugActions:
    """A container for methods used for in-game debugging.

    Args:
        game (Game): The main Game instance, used to access services and UI methods.
    """

    def __init__(self, game: "Game"):
        self._game = game

    def get_ds_file(self) -> None:
        """A debug method to fetch and display DSFile data."""
        # This ID is from data/ds_files.json
        test_file_id = DSFileId(uuid.UUID("a1b2c3d4-e5f6-4890-a234-567890abcdef"))
        dto = self._game.ds_file_service.get_ds_file_data(test_file_id)
        if dto:
            message = f"Found file: {dto.name} ({dto.size}KB, Type: {dto.file_type})"
            self._game.show_message(message)
        else:
            self._game.show_message("Test DSFile not found.")
