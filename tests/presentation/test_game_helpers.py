"""Tests for the Game class's helper methods."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.matrix_run_view import MatrixRunView
from decker_pygame.presentation.components.message_view import MessageView
from tests.presentation.conftest import Mocks


def test_game_update_sprites_no_modal(game_with_mocks: Mocks):
    """Tests that update_sprites calls update on all sprites when no modal is active."""
    mocks = game_with_mocks
    game = mocks.game
    game.view_manager.modal_stack.clear()

    # Create some mock sprites to iterate over
    mock_sprite1 = Mock(spec=pygame.sprite.Sprite)
    mock_sprite2 = Mock(spec=MatrixRunView)  # One of them is a MatrixRunView
    game.all_sprites.empty()
    game.all_sprites.add(mock_sprite1, mock_sprite2)

    # Configure the mock service to return a mock DTO
    mock_dto = Mock()
    mocks.matrix_run_service.get_matrix_run_view_data.return_value = mock_dto

    with patch(
        "decker_pygame.presentation.game.pygame.time.get_ticks", return_value=123000
    ):
        game.update_sprites(dt=0.016)

    # Assert that the service was called
    mocks.matrix_run_service.get_matrix_run_view_data.assert_called_once_with(
        game.character_id, game.player_id
    )
    # Assert that the DTO was updated
    assert mock_dto.run_time_in_seconds == 123  # 123000 ms / 1000

    # Assert that the update methods were called correctly
    mock_sprite1.update.assert_called_once_with(16)
    mock_sprite2.update.assert_called_once_with(mock_dto)


def test_game_update_sprites_with_modal(game_with_mocks: Mocks):
    """Tests that update_sprites calls update only on the top modal view."""
    mocks = game_with_mocks
    game = mocks.game

    # Create mock views for the modal stack
    modal_view1 = Mock(spec=pygame.sprite.Sprite)
    modal_view2 = Mock(spec=MatrixRunView)
    game.view_manager.modal_stack.extend([modal_view1, modal_view2])

    # Configure the mock service and time to return mock data
    mock_dto = Mock()
    mocks.matrix_run_service.get_matrix_run_view_data.return_value = mock_dto
    with patch(
        "decker_pygame.presentation.game.pygame.time.get_ticks", return_value=123000
    ):
        game.update_sprites(dt=0.016)

    # Assert that the service was called
    mocks.matrix_run_service.get_matrix_run_view_data.assert_called_once_with(
        game.character_id, game.player_id
    )
    # Assert that the DTO was updated
    assert mock_dto.run_time_in_seconds == 123

    # Assert that the update methods were called correctly
    modal_view1.update.assert_not_called()
    modal_view2.update.assert_called_once_with(mock_dto)


def test_game_update_sprites_with_non_matrix_modal(game_with_mocks: Mocks):
    """Tests that update_sprites calls update with dt on a non-MatrixRunView modal."""
    game = game_with_mocks.game

    modal_view1 = Mock(spec=pygame.sprite.Sprite)
    modal_view2 = Mock(spec=pygame.sprite.Sprite)  # Not a MatrixRunView
    game.view_manager.modal_stack.extend([modal_view1, modal_view2])

    game.update_sprites(dt=0.016)

    modal_view1.update.assert_not_called()
    modal_view2.update.assert_called_once_with(16)


def test_game_update_sprites_with_modal_without_update_method(game_with_mocks: Mocks):
    """Tests that update_sprites does not crash if a modal view has no update method."""
    game = game_with_mocks.game

    # Create a mock view that does NOT have an update method
    # by using a spec of an object without one.
    modal_view = Mock(spec=object())
    game.view_manager.modal_stack.append(modal_view)

    # This should execute without raising an AttributeError
    try:
        game.update_sprites(dt=0.016)
    except AttributeError:
        pytest.fail(
            "game.update_sprites crashed on a modal view without an update method"
        )


def test_game_show_message(game_with_mocks: Mocks):
    """Tests that the show_message method calls set_text on the message_view."""
    game = game_with_mocks.game
    # Replace the real view with a mock for this test
    game.message_view = Mock(spec=MessageView)

    game.show_message("Test message")

    game.message_view.set_text.assert_called_once_with("Test message")


def test_execute_and_refresh_view_success(game_with_mocks: Mocks):
    """
    Tests that _execute_and_refresh_view correctly executes action and toggles view
    on success.
    """
    game = game_with_mocks.game
    mock_action = Mock()
    mock_view_toggler = Mock()

    game._execute_and_refresh_view(mock_action, mock_view_toggler)

    mock_action.assert_called_once()
    assert mock_view_toggler.call_count == 2
    mock_view_toggler.assert_called_with()  # Ensure it was called without arguments


def test_execute_and_refresh_view_failure(game_with_mocks: Mocks):
    """
    Tests that _execute_and_refresh_view handles exceptions and does not toggle view
    on failure.
    """
    game = game_with_mocks.game
    mock_action = Mock(side_effect=ValueError("Test Error"))
    mock_view_toggler = Mock()

    with patch.object(game, "show_message") as mock_show_message:
        game._execute_and_refresh_view(mock_action, mock_view_toggler)

        mock_action.assert_called_once()
        mock_view_toggler.assert_not_called()
        mock_show_message.assert_called_once_with("Error: Test Error")
