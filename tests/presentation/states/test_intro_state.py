"""Tests for the IntroState class."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.game import Game
from decker_pygame.presentation.states.intro_state import IntroState
from decker_pygame.presentation.states.new_char_state import NewCharState


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object with a mock ViewManager."""
    game = Mock(spec=Game)
    game.view_manager = Mock()
    return game


@pytest.fixture
def intro_state(mock_game: Mock) -> IntroState:
    """Provides a IntroState instance with a mocked Game."""
    return IntroState(mock_game)


def test_enter_creates_and_shows_view(intro_state: IntroState, mock_game: Mock):
    """Tests that entering the state creates and shows the IntroView."""
    with patch(
        "decker_pygame.presentation.states.intro_state.IntroView"
    ) as mock_intro_view_class:
        intro_state.enter()

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args

        assert args[0] == "intro_view"
        factory = args[1]
        assert callable(factory)

        _ = factory()
        mock_intro_view_class.assert_called_once_with(
            on_continue=intro_state._on_continue
        )


def test_exit_closes_view(intro_state: IntroState, mock_game: Mock):
    """Tests that exiting the state closes the IntroView."""
    intro_state.exit()

    mock_game.view_manager.toggle_view.assert_called_once_with(
        "intro_view", None, mock_game
    )


def test_on_continue_transitions_state(intro_state: IntroState, mock_game: Mock):
    """Tests that the _on_continue callback transitions to the NewCharState."""
    intro_state._on_continue()

    mock_game.set_state.assert_called_once()
    call_args, _ = mock_game.set_state.call_args
    assert isinstance(call_args[0], NewCharState)


def test_handle_event_delegates_to_view_manager(
    intro_state: IntroState, mock_game: Mock
):
    """Tests that handle_event is delegated to the view manager."""
    event = pygame.event.Event(pygame.KEYDOWN)
    intro_state.handle_event(event)
    mock_game.view_manager.handle_event.assert_called_once_with(event)


def test_get_sprites_returns_empty_list(intro_state: IntroState):
    """Tests that get_sprites returns an empty list as the view manager handles sprites."""
    assert intro_state.get_sprites() == []
