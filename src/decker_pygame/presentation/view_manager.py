from collections.abc import Callable
from typing import Optional, TypeVar, cast

import pygame

from decker_pygame.presentation.protocols import Eventful

V = TypeVar("V", bound=pygame.sprite.Sprite)


class ViewManager:
    """Manages the display and interaction of UI views, including a modal stack."""

    def __init__(self, all_sprites: pygame.sprite.Group[pygame.sprite.Sprite]):
        self._all_sprites = all_sprites
        self._modal_stack: list[Eventful] = []

    def toggle_view(
        self,
        view_attr_name: str,
        view_factory: Callable[[], Optional[V]],
        game_instance: object,  # The Game instance where the view attribute resides
    ) -> Optional[V]:
        """Generic method to open or close a view.

        Args:
            view_attr_name (str): The name of the attribute on `game_instance` that
                holds the view instance.
            view_factory (Callable[[], Optional[V]]): A function that creates and
                returns a view instance, or None on failure.
            game_instance (object): The instance (e.g., Game) that owns the view
                attribute.
        """
        current_view = getattr(game_instance, view_attr_name, None)
        if current_view:
            self._all_sprites.remove(current_view)
            setattr(game_instance, view_attr_name, None)
            if hasattr(current_view, "handle_event"):
                eventful_view = cast(Eventful, current_view)
                if eventful_view in self._modal_stack:
                    self._modal_stack.remove(eventful_view)
            return None  # Return None when closing

        else:
            new_view = view_factory()
            if new_view:
                setattr(game_instance, view_attr_name, new_view)
                self._all_sprites.add(new_view)

                if hasattr(new_view, "handle_event"):
                    self._modal_stack.append(cast(Eventful, new_view))
            return new_view  # Return the new view when opening

    @property
    def top_modal_view(self) -> Optional[Eventful]:
        """Returns the top-most modal view, or None if the stack is empty."""
        return self._modal_stack[-1] if self._modal_stack else None
