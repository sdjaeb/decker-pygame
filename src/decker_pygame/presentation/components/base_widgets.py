"""This module provides base classes and mixins for UI components."""

from abc import ABC, abstractmethod
from collections.abc import Callable

import pygame


class Clickable(pygame.sprite.Sprite, ABC):
    """An abstract base class for any clickable UI element.

    Args:
        on_click (Callable[[], None]): A zero-argument function to call when clicked.

    Attributes:
        image (pygame.Surface): The surface that represents the clickable element.
        rect (pygame.Rect): The rectangular area of the element.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, on_click: Callable[[], None]):
        super().__init__()
        self._on_click = on_click

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a single pygame event to determine if a click occurred."""
        raise NotImplementedError  # pragma: no cover
