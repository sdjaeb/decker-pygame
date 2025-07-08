from collections.abc import Callable

import pygame

from decker_pygame.application.deck_service import DeckViewData


class DeckView(pygame.sprite.Sprite):
    """A UI component that displays the player's deck of programs."""

    def __init__(self, data: DeckViewData, on_close: Callable[[], None]) -> None:
        super().__init__()
        self._data = data
        self._on_close = on_close
