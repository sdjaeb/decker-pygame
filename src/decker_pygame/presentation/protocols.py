"""This module defines protocols for the presentation layer."""

from typing import Protocol

import pygame


class Eventful(Protocol):
    """A protocol for objects that can handle Pygame events."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles a single Pygame event.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        ...  # pragma: no cover


class BaseState(Protocol):
    """A protocol for all game states."""

    def enter(self) -> None:
        """Called when the state is entered."""
        ...  # pragma: no cover

    def exit(self) -> None:
        """Called when the state is exited."""
        ...  # pragma: no cover

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles a single Pygame event for the state.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        ...  # pragma: no cover

    def update(self, dt: int, total_seconds: int) -> None:
        """Updates the state logic.

        Args:
            dt (int): Time since last frame in milliseconds.
            total_seconds (int): Total time since game start in seconds.
        """
        ...  # pragma: no cover

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the state's components to the screen.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        """
        ...  # pragma: no cover
