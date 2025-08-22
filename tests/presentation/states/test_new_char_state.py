"""Tests for the NewCharState class."""

import uuid
from unittest.mock import Mock, patch

import pytest

from decker_pygame.domain.ids import CharacterId
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.states.home_state import HomeState
from decker_pygame.presentation.states.new_char_state import NewCharState


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object with mock services and a ViewManager."""
    game = Mock(spec=Game)
    game.view_manager = Mock()
    game.character_service = Mock()
    game.player_id = uuid.uuid4()
    return game


@pytest.fixture
def new_char_state(mock_game: Mock) -> NewCharState:
    """Provides a NewCharState instance with a mocked Game."""
    return NewCharState(mock_game)


def test_enter_creates_and_shows_view(new_char_state: NewCharState, mock_game: Mock):
    """Tests that entering the state creates and shows the NewCharView."""
    with patch(
        "decker_pygame.presentation.states.new_char_state.NewCharView"
    ) as mock_new_char_view_class:
        new_char_state.enter()

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args

        assert args[0] == "new_char_view"
        factory = args[1]
        assert callable(factory)

        _ = factory()
        mock_new_char_view_class.assert_called_once_with(
            on_create=new_char_state._handle_character_creation
        )


def test_exit_closes_view(new_char_state: NewCharState, mock_game: Mock):
    """Tests that exiting the state closes the NewCharView."""
    new_char_state.exit()

    mock_game.view_manager.toggle_view.assert_called_once_with(
        "new_char_view", None, mock_game
    )


def test_handle_character_creation_transitions_state(
    new_char_state: NewCharState, mock_game: Mock
):
    """Tests that the character creation callback transitions to the HomeState."""
    char_name = "Test Decker"
    new_id = CharacterId(uuid.uuid4())
    mock_game.character_service.create_character.return_value = new_id

    new_char_state._handle_character_creation(char_name)

    mock_game.character_service.create_character.assert_called_once_with(
        mock_game.player_id, char_name
    )
    assert mock_game.character_id == new_id
    mock_game.show_message.assert_called_once_with(f"Welcome, {char_name}.")

    mock_game.set_state.assert_called_once()
    call_args, _ = mock_game.set_state.call_args
    assert isinstance(call_args[0], HomeState)


def test_get_sprites_returns_empty_list(new_char_state: NewCharState):
    """Tests that get_sprites returns an empty list."""
    assert new_char_state.get_sprites() == []
