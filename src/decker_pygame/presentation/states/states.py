"""This module contains the concrete implementations of the game states."""

from typing import TYPE_CHECKING

import pygame

from decker_pygame.presentation.states.game_states import BaseState

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class IntroState(BaseState):
    """The state for the game's introduction sequence."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def on_enter(self) -> None:
        """Open the intro view when entering this state."""
        self.game.toggle_intro_view()

    def on_exit(self) -> None:
        """Close the intro view when exiting this state."""
        if self.game.intro_view:
            self.game.toggle_intro_view()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the modal view."""

    def update(self, dt: float) -> None:
        """State logic is handled by the modal view."""

    def draw(self, screen: pygame.Surface) -> None:
        """Drawing is handled by the main game loop's sprite group."""


class NewCharState(BaseState):
    """The state for creating a new character."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def on_enter(self) -> None:
        """Open the new character view when entering this state."""
        self.game.toggle_new_char_view()

    def on_exit(self) -> None:
        """Close the new character view when exiting this state."""
        if self.game.new_char_view:
            self.game.toggle_new_char_view()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the modal view."""

    def update(self, dt: float) -> None:
        """State logic is handled by the modal view."""

    def draw(self, screen: pygame.Surface) -> None:
        """Drawing is handled by the main game loop's sprite group."""


class HomeState(BaseState):
    """The main hub state of the game."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def on_enter(self) -> None:
        """Open the home view when entering this state."""
        self.game.toggle_home_view()

    def on_exit(self) -> None:
        """Close the home view when exiting this state."""
        if self.game.home_view:
            self.game.toggle_home_view()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the modal view."""

    def update(self, dt: float) -> None:
        """State logic is handled by the modal view."""

    def draw(self, screen: pygame.Surface) -> None:
        """Drawing is handled by the main game loop's sprite group."""


class MatrixRunState(BaseState):
    """The state for an active matrix run."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def on_enter(self) -> None:
        """Open the matrix run view when entering this state."""
        self.game.toggle_matrix_run_view()

    def on_exit(self) -> None:
        """Close the matrix run view when exiting this state."""
        if self.game.matrix_run_view:
            self.game.toggle_matrix_run_view()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the modal view."""

    def update(self, dt: float) -> None:
        """State logic is handled by the modal view."""

    def draw(self, screen: pygame.Surface) -> None:
        """Drawing is handled by the main game loop's sprite group."""
