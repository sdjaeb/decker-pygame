"""Tests for the concrete game state classes and their base protocol."""

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.states.game_states import BaseState
from decker_pygame.presentation.states.states import (
    HomeState,
    IntroState,
    MatrixRunState,
    NewCharState,
)

if TYPE_CHECKING:
    from decker_pygame.presentation.game import Game


class DummyState(BaseState):
    """A concrete class for testing the BaseState protocol for coverage."""

    def __init__(self, game: "Game") -> None:
        """Initializes the dummy state."""

    def on_enter(self) -> None:
        """Dummy on_enter."""

    def on_exit(self) -> None:
        """Dummy on_exit."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Dummy handle_event."""

    def update(self, dt: float) -> None:
        """Dummy update."""

    def draw(self, screen: pygame.Surface) -> None:
        """Dummy draw."""


def test_base_state_protocol_coverage() -> None:
    """This test exists purely to satisfy coverage for the protocol definition."""
    mock_game = Mock()
    state = DummyState(mock_game)
    state.on_enter()
    state.on_exit()
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.1)
    state.draw(Mock(spec=pygame.Surface))


@pytest.mark.parametrize(
    ("state_class", "toggle_method_name", "view_attribute_name"),
    [
        (IntroState, "toggle_intro_view", "intro_view"),
        (NewCharState, "toggle_new_char_view", "new_char_view"),
        (HomeState, "toggle_home_view", "home_view"),
        (MatrixRunState, "toggle_matrix_run_view", "matrix_run_view"),
    ],
)
def test_concrete_states(
    state_class: type[BaseState],
    toggle_method_name: str,
    view_attribute_name: str,
) -> None:
    """
    Tests the lifecycle and empty methods of concrete game states.

    This test verifies that:
    - on_enter calls the correct view toggling method.
    - on_exit correctly handles closing an open or already-closed view.
    - The handle_event, update, and draw methods can be called without error
      (for coverage).
    """
    mock_game = Mock()
    state = state_class(mock_game)
    mock_toggle_method = getattr(mock_game, toggle_method_name)

    # --- Test on_enter ---
    state.on_enter()
    mock_toggle_method.assert_called_once()

    # --- Test on_exit ---
    # When view is open
    setattr(mock_game, view_attribute_name, Mock())
    state.on_exit()
    assert mock_toggle_method.call_count == 2

    # When view is already closed
    mock_toggle_method.reset_mock()
    setattr(mock_game, view_attribute_name, None)
    state.on_exit()
    mock_toggle_method.assert_not_called()

    # --- Test empty methods for coverage ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.16)
    state.draw(Mock(spec=pygame.Surface))
