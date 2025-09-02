"""This module defines debug actions for the presentation layer."""

from typing import TYPE_CHECKING

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.events import MatrixLogEntryCreated
from decker_pygame.presentation.states.game_states import GameState

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class DebugActions:
    """A container for debugging actions that can be triggered by key presses."""

    def __init__(self, game: "Game", event_dispatcher: EventDispatcher):
        self._game = game
        self._event_dispatcher = event_dispatcher

    def toggle_home_view(self) -> None:
        """Toggles the main home view."""
        self._game.set_state(GameState.HOME)

    def log_matrix_event(self) -> None:
        """Dispatches a sample matrix log event for debugging."""
        event = MatrixLogEntryCreated(message="[DEBUG] ICE Detected: Sentry v2.0")
        self._event_dispatcher.dispatch([event])
        self._game.show_message("Dispatched debug matrix event.")
