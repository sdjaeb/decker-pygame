"""This module contains actions used for debugging purposes."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class DebugActions:
    """A container for methods used for in-game debugging.

    Args:
        game (Game): The main Game instance.
    """

    def __init__(self, game: "Game"):
        self._game = game
