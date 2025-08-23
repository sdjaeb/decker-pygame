"""This module defines the ViewManager class."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Optional, TypeVar, cast

import pygame

from decker_pygame.presentation.protocols import Eventful

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game

V = TypeVar("V", bound=pygame.sprite.Sprite)


class ViewManager:
    """Manages the lifecycle of UI views, including modal focus."""

    def __init__(self, game: "Game") -> None:
        self._game = game
        self._modal_stack: list[Eventful] = []

    @property
    def modal_stack(self) -> list[Eventful]:
        """The stack of modal views that have input focus."""
        return self._modal_stack

    def toggle_view(
        self,
        view_attr: str,
        view_factory: Callable[[], Optional[V]],
    ) -> None:
        """Generic method to open or close a view."""
        current_view = getattr(self._game, view_attr)
        if current_view:
            self._game.all_sprites.remove(current_view)
            setattr(self._game, view_attr, None)
            if hasattr(current_view, "handle_event"):
                eventful_view = cast(Eventful, current_view)
                if eventful_view in self._modal_stack:
                    self._modal_stack.remove(eventful_view)
        else:
            new_view = view_factory()
            if new_view:
                setattr(self._game, view_attr, new_view)
                self._game.all_sprites.add(new_view)
                if hasattr(new_view, "handle_event"):
                    self._modal_stack.append(cast(Eventful, new_view))
