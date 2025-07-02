import uuid
from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.services import PlayerService
from decker_pygame.domain.model import PlayerId
from decker_pygame.presentation.game import Game


@pytest.fixture
def mocked_game_instance() -> Generator[Game]:
    """
    Provides a fully mocked Game instance suitable for unit testing,
    injecting a mock PlayerService.
    """
    mock_player_service = Mock(spec=PlayerService)
    dummy_player_id = PlayerId(uuid.uuid4())

    # Mock all external dependencies called in Game.__init__ and Game.run
    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.display.flip"),
        patch("pygame.time.Clock"),
        patch(
            "decker_pygame.presentation.game.load_spritesheet", return_value=([], [])
        ),
    ):
        yield Game(player_service=mock_player_service, player_id=dummy_player_id)


def test_game_initialization(mocked_game_instance: Game):
    """Tests that the Game class correctly stores its injected dependencies."""
    game = mocked_game_instance

    # The __init__ method should store the service and id
    assert isinstance(game.player_service, PlayerService)
    assert isinstance(game.player_id, uuid.UUID)

    # Pygame should be initialized
    pygame.init.assert_called_once()
    pygame.display.set_mode.assert_called_once()
    pygame.display.set_caption.assert_called_once()


def test_game_run_loop_quits(mocked_game_instance: Game):
    """Tests that the main game loop runs and can be exited via a QUIT event."""
    game = mocked_game_instance
    # Mock event.get to return a QUIT event on the first call.
    with patch(
        "pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)]
    ) as mock_event_get:
        # The __init__ method sets this to True.
        assert game.is_running is True

        # The loop should run once, process the QUIT event, and terminate.
        game.run()

        assert game.is_running is False
        mock_event_get.assert_called_once()


def test_game_update(mocked_game_instance: Game):
    """Tests that the _update method calls update on its sprite group."""
    game = mocked_game_instance
    game.all_sprites = Mock()

    game._update()

    game.all_sprites.update.assert_called_once()
