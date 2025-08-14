"""This module contains tests for the DebugActions class."""

import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.dtos import DSFileDTO
from decker_pygame.domain.ids import DSFileId
from decker_pygame.presentation.debug_actions import DebugActions
from decker_pygame.presentation.game import Game


@pytest.fixture
def mock_game() -> Mock:
    """Fixture for a mocked Game instance."""
    game = Mock(spec=Game)
    game.ds_file_service = Mock()
    game.show_message = Mock()
    return game


def test_get_ds_file_found(mock_game: Mock):
    """Tests that get_ds_file shows a message when the file is found."""
    actions = DebugActions(mock_game)
    test_id = DSFileId(uuid.UUID("a1b2c3d4-e5f6-4890-a234-567890abcdef"))
    dto = DSFileDTO(id=test_id, name="test.dat", file_type="data", size=1024)
    mock_game.ds_file_service.get_ds_file_data.return_value = dto

    actions.get_ds_file()

    mock_game.ds_file_service.get_ds_file_data.assert_called_once_with(test_id)
    mock_game.show_message.assert_called_once_with(
        "Found file: test.dat (1024KB, Type: data)"
    )


def test_get_ds_file_not_found(mock_game: Mock):
    """Tests that get_ds_file shows a message when the file is not found."""
    actions = DebugActions(mock_game)
    test_id = DSFileId(uuid.UUID("a1b2c3d4-e5f6-4890-a234-567890abcdef"))
    mock_game.ds_file_service.get_ds_file_data.return_value = None

    actions.get_ds_file()

    mock_game.ds_file_service.get_ds_file_data.assert_called_once_with(test_id)
    mock_game.show_message.assert_called_once_with("Test DSFile not found.")
