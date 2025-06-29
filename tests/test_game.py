import pygame
import pytest
from decker_pygame.game import Game
from decker_pygame.settings import TITLE
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_game_dependencies(mocker: MockerFixture) -> None:
    """Mock all external dependencies for the Game class."""
    mocker.patch("pygame.init")
    mocker.patch("pygame.display.set_mode")
    mocker.patch("pygame.display.set_caption")
    mocker.patch("pygame.display.flip")
    mocker.patch("pygame.quit")
    mocker.patch("pygame.sprite.Group")
    mocker.patch("decker_pygame.game.load_images", return_value=[])
    mocker.patch("pygame.time.Clock")
    mocker.patch("pygame.event.get", return_value=[])


def test_game_initialization() -> None:
    """Test that the Game class initializes correctly."""
    game = Game()
    assert game.is_running is True
    pygame.init.assert_called_once()
    pygame.display.set_mode.assert_called_once()
    pygame.display.set_caption.assert_called_with(TITLE)


def test_game_handle_events_quit() -> None:
    """Test that the game quits on a QUIT event."""
    pygame.event.get.return_value = [pygame.event.Event(pygame.QUIT)]
    game = Game()
    game._handle_events()
    assert game.is_running is False


def test_game_run_loop_exits(
    mocker: MockerFixture,
) -> None:
    """Test that the main game loop runs once and exits."""
    game = Game()

    # Make the loop run only once by setting is_running to False when events are handled
    mocker.patch.object(
        game, "_handle_events", side_effect=lambda: setattr(game, "is_running", False)
    )

    game.run()
    game._handle_events.assert_called_once()
    pygame.quit.assert_called_once()
