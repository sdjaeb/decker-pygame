"""This module contains the concrete implementations of the game states."""

from typing import TYPE_CHECKING

import pygame

from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.matrix_run_view import MatrixRunView
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.states.game_states import BaseState

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class IntroState(BaseState):
    """The state for the game's introduction sequence."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> IntroView:
        """Factory function to create the IntroView."""
        return IntroView(on_continue=self.game._continue_from_intro)

    def on_enter(self) -> None:
        """Open the intro view when entering this state."""
        self.game.view_manager.toggle_view("intro_view", self._factory)

    def on_exit(self) -> None:
        """Close the intro view when exiting this state."""
        # Calling toggle_view on an existing view will close it.
        self.game.view_manager.toggle_view("intro_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)


class NewCharState(BaseState):
    """The state for creating a new character."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> NewCharView:
        """Factory function to create the NewCharView."""
        return NewCharView(on_create=self.game._handle_character_creation)

    def on_enter(self) -> None:
        """Open the new character view when entering this state."""
        self.game.view_manager.toggle_view("new_char_view", self._factory)

    def on_exit(self) -> None:
        """Close the new character view when exiting this state."""
        # Calling toggle_view on an existing view will close it.
        self.game.view_manager.toggle_view("new_char_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)


class HomeState(BaseState):
    """The main hub state of the game."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> HomeView:
        """Factory function to create the HomeView."""
        return HomeView(
            on_char=self.game.toggle_char_data_view,
            on_deck=self.game.toggle_deck_view,
            on_contracts=self.game.toggle_contract_list_view,
            on_build=self.game.toggle_build_view,
            on_shop=self.game.toggle_shop_view,
            on_transfer=self.game.toggle_transfer_view,
            on_projects=self.game.toggle_project_data_view,
        )

    def on_enter(self) -> None:
        """Open the home view when entering this state."""
        self.game.view_manager.toggle_view("home_view", self._factory)

    def on_exit(self) -> None:
        """Close the home view when exiting this state."""
        self.game.view_manager.toggle_view("home_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)


class MatrixRunState(BaseState):
    """The state for an active matrix run."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> MatrixRunView:
        """Factory function to create the MatrixRunView."""
        return MatrixRunView(asset_service=self.game.asset_service)

    def on_enter(self) -> None:
        """Open the matrix run view when entering this state."""
        self.game.view_manager.toggle_view("matrix_run_view", self._factory)

    def on_exit(self) -> None:
        """Close the matrix run view when exiting this state."""
        self.game.view_manager.toggle_view("matrix_run_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)
