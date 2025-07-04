import uuid
from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.player_service import PlayerService
from decker_pygame.domain.player import PlayerId
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


def test_game_load_assets_with_icons():
    """Tests that asset loading correctly scales icons when they are present."""
    # This test needs its own setup to override the fixture's mock
    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.time.Clock"),
        patch("decker_pygame.presentation.game.load_spritesheet") as mock_load,
        patch("pygame.transform.scale") as mock_scale,
    ):
        # Simulate finding one icon
        mock_icon = Mock(spec=pygame.Surface)
        mock_load.return_value = ([mock_icon], (16, 16))

        # We don't need a real service or ID for this test
        game = Game(player_service=Mock(), player_id=Mock())

        # Assert that the scaling logic was called
        mock_load.assert_called_once()
        mock_scale.assert_called_once()
        assert len(game.active_bar._image_list) == 1


def test_game_run_loop_quits(mocked_game_instance: Game):
    """Tests that the main game loop runs, calls its methods, and can be exited."""
    game = mocked_game_instance
    # side_effect makes the mock return different values on subsequent calls.
    # 1st call: no events (loop runs). 2nd call: QUIT event (loop terminates).
    with (
        patch(
            "pygame.event.get", side_effect=[[], [pygame.event.Event(pygame.QUIT)]]
        ) as mock_event_get,
        patch("pygame.quit") as mock_quit,
    ):
        # Spy on _update and mock the draw method of the sprite group
        with (
            patch.object(game, "_update", wraps=game._update) as spy_update,
            patch.object(game.all_sprites, "draw") as mock_draw,
        ):
            # Mock the fill method so we can check call_count
            game.screen.fill = Mock()
            # Mock the clock.tick method to track call_count
            game.clock.tick = Mock()

            assert game.is_running is True

            game.run()

            # Loop should terminate
            assert game.is_running is False
            assert mock_event_get.call_count == 2

            # Check that the loop's contents were executed
            assert spy_update.call_count == 2
            assert game.screen.fill.call_count == 2
            assert mock_draw.call_count == 2
            pygame.display.flip.assert_called_with()
            assert game.clock.tick.call_count == 2

            # Check that quit was called after the loop
            mock_quit.assert_called_once()


def test_game_update(mocked_game_instance: Game):
    """Tests that the _update method calls update on its sprite group."""
    game = mocked_game_instance
    game.all_sprites = Mock()

    game._update()

    game.all_sprites.update.assert_called_once()
