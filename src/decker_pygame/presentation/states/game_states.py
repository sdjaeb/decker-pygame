"""This module defines the game state machine's core components."""

from enum import Enum, auto
from typing import TYPE_CHECKING, Protocol

from pygame import Surface, event

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class GameState(Enum):
    """Enumeration of all possible game states."""

    INTRO = auto()
    NEW_CHAR = auto()
    HOME = auto()
    MATRIX_RUN = auto()
    QUIT = auto()


class BaseState(Protocol):
    """Protocol defining the interface for all game states."""

    def __init__(self, game: "Game") -> None: ...

    def on_enter(self) -> None:
        """Code to run when entering this state."""
        ...

    def on_exit(self) -> None:
        """Code to run when exiting this state."""
        ...

    def handle_event(self, event: event.Event) -> None:
        """Handle user input and other events."""
        ...

    def update(self, dt: float) -> None:
        """Update game logic for the current state."""
        ...

    def draw(self, screen: Surface) -> None:
        """Draw the current state to the screen."""
        ...
