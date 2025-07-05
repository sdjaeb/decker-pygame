import uuid
from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.crafting_service import CraftingError, CraftingService
from decker_pygame.application.player_service import PlayerService
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.game import Game


@pytest.fixture(autouse=True)
def pygame_context() -> Generator[None]:
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game_with_mocks() -> Generator[tuple[Game, Mock, Mock]]:
    """
    Provides a fully mocked Game instance and its mocked dependencies.
    """
    mock_player_service = Mock(autospec=PlayerService)
    mock_crafting_service = Mock(autospec=CraftingService)
    dummy_player_id = PlayerId(uuid.uuid4())
    dummy_character_id = CharacterId(uuid.uuid4())

    # Mock all external dependencies called in Game.__init__ and Game.run
    with (
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.display.flip"),
        patch("pygame.time.Clock"),
        patch(
            "decker_pygame.presentation.game.load_spritesheet",
            return_value=([pygame.Surface((16, 16))], (16, 16)),
        ),
        patch("decker_pygame.presentation.game.pygame.transform.scale"),
    ):
        game = Game(
            player_service=mock_player_service,
            player_id=dummy_player_id,
            crafting_service=mock_crafting_service,
            character_id=dummy_character_id,
        )
        yield game, mock_player_service, mock_crafting_service


def test_game_initialization(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests that the Game class correctly stores its injected dependencies."""
    game, mock_player_service, mock_crafting_service = game_with_mocks

    # The __init__ method should store the service and id
    assert game.player_service is mock_player_service
    assert game.crafting_service is mock_crafting_service
    assert isinstance(game.player_id, uuid.UUID)
    assert isinstance(game.character_id, uuid.UUID)
    assert isinstance(game.message_view, MessageView)

    pygame.display.set_mode.assert_called_once()
    pygame.display.set_caption.assert_called_once()


def test_game_load_assets_with_icons():
    """Tests that asset loading correctly scales icons when they are present."""
    # This test needs its own setup to override the fixture's mock
    with (
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.time.Clock"),
        patch("decker_pygame.presentation.game.load_spritesheet") as mock_load,
        patch("decker_pygame.presentation.game.pygame.transform.scale") as mock_scale,
    ):
        # Simulate finding one icon
        mock_icon = pygame.Surface((16, 16))
        mock_load.return_value = ([mock_icon], (16, 16))

        # We don't need a real service or ID for this test
        game = Game(
            player_service=Mock(autospec=PlayerService),
            player_id=Mock(spec=PlayerId),
            crafting_service=Mock(autospec=CraftingService),
            character_id=Mock(spec=CharacterId),
        )

        # Assert that the scaling logic was called
        mock_load.assert_called_once()
        mock_scale.assert_called_once()
        assert len(game.active_bar._image_list) == 1


def test_game_run_loop_quits(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests that the main game loop runs, calls its methods, and can be exited."""
    game, _, _ = game_with_mocks

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


def test_game_update(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests that the _update method calls update on its sprite group."""
    game, _, _ = game_with_mocks
    game.all_sprites = Mock()

    game._update()

    game.all_sprites.update.assert_called_once()


def test_game_show_message(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests that the show_message method calls set_text on the message_view."""
    game, _, _ = game_with_mocks
    # Replace the real view with a mock for this test
    game.message_view = Mock(spec=MessageView)

    game.show_message("Test message")

    game.message_view.set_text.assert_called_once_with("Test message")


def test_game_toggles_build_view(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests that pressing 'b' opens and closes the build view."""
    game, _, mock_crafting_service = game_with_mocks
    # Ensure the service returns schematics so the view can be created
    mock_crafting_service.get_character_schematics.return_value = [Mock()]

    assert game.build_view is None

    # Press 'b' to open the view
    open_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_b})
    with patch("pygame.event.get", return_value=[open_event]):
        with patch(
            "decker_pygame.presentation.game.BuildView", spec=BuildView
        ) as mock_build_view_class:
            game._handle_events()
            mock_build_view_class.assert_called_once()
            assert game.build_view is not None
            assert game.build_view in game.all_sprites

    # Press 'b' again to close the view
    close_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_b})
    with patch("pygame.event.get", return_value=[close_event]):
        game._handle_events()
        assert game.build_view is None
        # Check that the sprite was removed from the group
        assert len(game.all_sprites) == 3  # active_bar, alarm_bar, message_view


def test_game_build_view_event_handling(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests that the game correctly delegates events to an active build view."""
    game, _, _ = game_with_mocks
    game.build_view = Mock(spec=BuildView)  # Manually set an active view

    mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})
    with patch("pygame.event.get", return_value=[mouse_event]):
        game._handle_events()

    game.build_view.handle_event.assert_called_once_with(mouse_event)


def test_game_handle_build_click(game_with_mocks: tuple[Game, Mock, Mock]):
    """Tests the callback function that handles build clicks."""
    game, _, mock_crafting_service = game_with_mocks
    schematic_name = "TestSchematic"

    # Test success case
    game._handle_build_click(schematic_name)
    mock_crafting_service.craft_item.assert_called_once_with(
        game.character_id, schematic_name
    )

    # Test failure case
    mock_crafting_service.craft_item.reset_mock()
    mock_crafting_service.craft_item.side_effect = CraftingError("Test Error")
    game._handle_build_click(schematic_name)
    mock_crafting_service.craft_item.assert_called_once_with(
        game.character_id, schematic_name
    )
