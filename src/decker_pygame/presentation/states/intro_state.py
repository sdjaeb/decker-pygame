from typing import TYPE_CHECKING

import pygame

from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.protocols import BaseState
from decker_pygame.presentation.states.new_char_state import NewCharState  # New import

if TYPE_CHECKING:
    from decker_pygame.presentation.game import Game
    from decker_pygame.presentation.view_manager import View


class IntroState(BaseState):
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.intro_view: View = None

    def _on_continue(self) -> None:
        """Callback to transition to the next state."""
        self.game.set_state(NewCharState(self.game))

    def enter(self) -> None:
        """Create and show the IntroView when entering the state."""

        def factory() -> IntroView:
            return IntroView(on_continue=self._on_continue)

        self.intro_view = self.game.view_manager.toggle_view(
            "intro_view", factory, self.game
        )

    def exit(self) -> None:
        """Close the IntroView when exiting the state."""
        self.game.view_manager.toggle_view("intro_view", None, self.game)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.game.view_manager.handle_event(event)

    def update(self, dt: int, total_seconds: int) -> None:
        self.game.view_manager.update(dt, total_seconds)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.view_manager.draw(screen)

    def get_sprites(self) -> list[pygame.sprite.Sprite]:
        # Sprites are now managed by the ViewManager, so the state doesn't need to.
        return []
