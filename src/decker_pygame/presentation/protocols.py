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
