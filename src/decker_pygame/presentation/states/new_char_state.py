from typing import TYPE_CHECKING

import pygame

from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.protocols import BaseState
from decker_pygame.presentation.states.home_state import HomeState

if TYPE_CHECKING:
    from decker_pygame.presentation.game import Game
    from decker_pygame.presentation.view_manager import View


class NewCharState(BaseState):
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.new_char_view: View = None

    def _handle_character_creation(self, name: str) -> None:
        """Handles the creation of a new character, then transitions to home."""
        new_char_id = self.game.character_service.create_character(
            self.game.player_id, name
        )
        self.game.character_id = new_char_id
        self.game.show_message(f"Welcome, {name}.")

        self.game.set_state(HomeState(self.game))

    def enter(self) -> None:
        """Create and show the NewCharView when entering the state."""

        def factory() -> NewCharView:
            return NewCharView(on_create=self._handle_character_creation)

        self.new_char_view = self.game.view_manager.toggle_view(
            "new_char_view", factory, self.game
        )

    def exit(self) -> None:
        """Close the NewCharView when exiting the state."""
        self.game.view_manager.toggle_view("new_char_view", None, self.game)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.game.view_manager.handle_event(event)

    def update(self, dt: int, total_seconds: int) -> None:
        self.game.view_manager.update(dt, total_seconds)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.view_manager.draw(screen)

    def get_sprites(self) -> list[pygame.sprite.Sprite]:
        # Sprites are now managed by the ViewManager, so the state doesn't need to.
        return []
