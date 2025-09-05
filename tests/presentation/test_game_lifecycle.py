"""Tests for the core lifecycle and state machine of the Game class."""

from typing import cast
from unittest.mock import Mock, patch

from decker_pygame.presentation.states.game_states import BaseState, GameState
from decker_pygame.presentation.states.states import (
    IntroState,
)
from decker_pygame.settings import FPS
from tests.presentation.conftest import Mocks


def test_game_initialization(game_with_mocks: Mocks):
    """Tests that the Game class correctly stores its injected dependencies."""
    mocks = game_with_mocks
    game = mocks.game

    # The __init__ method should store the service and id
    assert game.asset_service is mocks.asset_service
    assert game.player_service is mocks.player_service
    assert game.character_service is mocks.character_service
    assert game.contract_service is mocks.contract_service
    assert game.crafting_service is mocks.crafting_service
    assert game.deck_service is mocks.deck_service
    assert game.ds_file_service is mocks.ds_file_service
    assert game.shop_service is mocks.shop_service
    assert game.node_service is mocks.node_service
    assert game.settings_service is mocks.settings_service
    assert game.project_service is mocks.project_service
    assert game.logging_service is mocks.logging_service
    assert game.event_dispatcher is mocks.event_dispatcher
    # State machine attributes
    assert len(game.states) == 4
    assert game.states[GameState.INTRO] is IntroState
    assert isinstance(game.current_state, IntroState)


def test_run_loop_calls_methods(game_with_mocks: Mocks):
    """Tests that the main loop calls its core methods."""
    game = game_with_mocks.game

    # Configure mock input handler to quit the game on the first call.
    game.input_handler.handle_events.side_effect = game.quit  # type: ignore[attr-defined]
    game.clock.tick.return_value = 16  # type: ignore[attr-defined]

    # Mock the current state to check for calls
    mock_state = Mock(spec=BaseState)
    game.current_state = mock_state

    game.run()

    game.input_handler.handle_events.assert_called_once()  # type: ignore[attr-defined]
    mock_state.update.assert_called_once_with(0.016)  # dt in seconds
    mock_state.draw.assert_called_once_with(game.screen)
    game.clock.tick.assert_called_once_with(FPS)  # type: ignore[attr-defined]


def test_game_quit_method(game_with_mocks: Mocks):
    """Tests that the public quit() method sets the is_running flag to False."""
    game = game_with_mocks.game
    assert game.is_running is True
    game.quit()
    assert game.is_running is False


def test_set_state_transitions_correctly(game_with_mocks: Mocks):
    """Tests that set_state calls on_exit and on_enter on the correct states."""
    game = game_with_mocks.game

    # Create mock state classes
    mock_state_a_instance = Mock(spec=BaseState)
    mock_state_a_class = Mock(return_value=mock_state_a_instance)

    mock_state_b_instance = Mock(spec=BaseState)
    mock_state_b_class = Mock(return_value=mock_state_b_instance)

    # Register the mock states
    game.states = {
        GameState.INTRO: cast(type[BaseState], mock_state_a_class),
        GameState.HOME: cast(type[BaseState], mock_state_b_class),
    }

    # --- Transition 1: from None to State A ---
    game.set_state(GameState.INTRO)

    # Assert State A was created and entered
    mock_state_a_class.assert_called_once_with(game)
    assert game.current_state is mock_state_a_instance
    mock_state_a_instance.on_enter.assert_called_once()
    mock_state_a_instance.on_exit.assert_not_called()

    # --- Transition 2: from State A to State B ---
    game.set_state(GameState.HOME)

    # Assert State A was exited
    mock_state_a_instance.on_exit.assert_called_once()

    # Assert State B was created and entered
    mock_state_b_class.assert_called_once_with(game)
    assert game.current_state is mock_state_b_instance
    mock_state_b_instance.on_enter.assert_called_once()


def test_set_state_to_quit(game_with_mocks: Mocks):
    """Tests that setting the state to QUIT calls the game's quit method."""
    game = game_with_mocks.game
    with patch.object(game, "quit") as mock_quit:
        game.set_state(GameState.QUIT)
        mock_quit.assert_called_once()


def test_set_state_to_unregistered_state_quits(game_with_mocks: Mocks):
    """Tests that setting the state to an unregistered enum quits the game."""
    game = game_with_mocks.game
    game.states = {}  # Ensure the state is not registered
    with patch.object(game, "quit") as mock_quit:
        game.set_state(GameState.MATRIX_RUN)
        mock_quit.assert_called_once()


def test_continue_from_intro_sets_state(game_with_mocks: Mocks):
    """Tests that _continue_from_intro transitions to the NEW_CHAR state."""
    game = game_with_mocks.game
    with patch.object(game, "set_state") as mock_set_state:
        game._continue_from_intro()
        mock_set_state.assert_called_once_with(GameState.NEW_CHAR)


def test_handle_character_creation_sets_state(game_with_mocks: Mocks):
    """Tests that _handle_character_creation transitions to the HOME state."""
    mocks = game_with_mocks
    game = mocks.game
    with patch.object(game, "set_state") as mock_set_state:
        game._handle_character_creation("Decker")
        mocks.logging_service.log.assert_called_once_with(
            "Character Creation", {"name": "Decker"}
        )
        mock_set_state.assert_called_once_with(GameState.HOME)
