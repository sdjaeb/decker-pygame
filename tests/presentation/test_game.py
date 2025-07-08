import uuid
from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.character_service import CharacterDataDTO
from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.application.player_service import PlayerStatusDTO
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    LoggingServiceInterface,
    PlayerServiceInterface,
)
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.char_data_view import CharDataView
from decker_pygame.presentation.components.health_bar import HealthBar
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.game import Game
from decker_pygame.settings import GFX


@pytest.fixture(autouse=True)
def pygame_context() -> Generator[None]:
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game_with_mocks() -> Generator[tuple[Game, Mock, Mock, Mock, Mock, Mock]]:
    """
    Provides a fully mocked Game instance and its mocked dependencies.
    """
    mock_player_service = Mock(spec=PlayerServiceInterface)
    mock_character_service = Mock(spec=CharacterServiceInterface)
    mock_contract_service = Mock(spec=ContractServiceInterface)
    mock_crafting_service = Mock(spec=CraftingServiceInterface)
    mock_logging_service = Mock(spec=LoggingServiceInterface)
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
        patch("decker_pygame.presentation.game.scale_icons") as mock_scale_icons,
    ):
        game = Game(
            player_service=mock_player_service,
            player_id=dummy_player_id,
            character_service=mock_character_service,
            contract_service=mock_contract_service,
            crafting_service=mock_crafting_service,
            character_id=dummy_character_id,
            logging_service=mock_logging_service,
        )
        mock_scale_icons.return_value = [pygame.Surface((32, 32))]
        yield (
            game,
            mock_player_service,
            mock_character_service,
            mock_contract_service,
            mock_crafting_service,
            mock_logging_service,
        )


def test_game_initialization(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that the Game class correctly stores its injected dependencies."""
    (
        game,
        mock_player_service,
        mock_character_service,
        mock_contract_service,
        mock_crafting_service,
        mock_logging_service,
    ) = game_with_mocks

    # The __init__ method should store the service and id
    assert game.player_service is mock_player_service
    assert game.character_service is mock_character_service
    assert game.contract_service is mock_contract_service
    assert game.crafting_service is mock_crafting_service
    assert game.logging_service is mock_logging_service
    assert isinstance(game.player_id, uuid.UUID)
    assert isinstance(game.character_id, uuid.UUID)
    assert isinstance(game.message_view, MessageView)
    assert isinstance(game.health_bar, HealthBar)

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
        patch("decker_pygame.presentation.game.scale_icons") as mock_scale_icons,
    ):
        # Simulate finding one icon
        mock_icon = pygame.Surface((16, 16))
        mock_load.return_value = ([mock_icon], (16, 16))
        mock_scale_icons.return_value = [pygame.Surface((32, 32))]

        # We don't need a real service or ID for this test
        game = Game(
            player_service=Mock(spec=PlayerServiceInterface),
            player_id=Mock(spec=PlayerId),
            character_service=Mock(spec=CharacterServiceInterface),
            contract_service=Mock(spec=ContractServiceInterface),
            crafting_service=Mock(spec=CraftingServiceInterface),
            character_id=Mock(spec=CharacterId),
            logging_service=Mock(spec=LoggingServiceInterface),
        )

        # Assert that the scaling logic was called
        mock_load.assert_called_once()
        mock_scale_icons.assert_called_once_with(
            [mock_icon],
            (GFX.active_bar_image_size, GFX.active_bar_image_size),
        )
        assert len(game.active_bar._image_list) == 1


def test_game_load_assets_no_icons():
    """Tests that asset loading handles the case where no icons are found."""
    # This test needs its own setup to override the fixture's mock
    with (
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.time.Clock"),
        patch("decker_pygame.presentation.game.load_spritesheet") as mock_load,
        patch("decker_pygame.presentation.game.scale_icons") as mock_scale_icons,
        # We also patch ActiveBar to prevent it from raising an error on an empty list
        patch("decker_pygame.presentation.game.ActiveBar") as mock_active_bar,
    ):
        # Simulate finding no icons
        mock_load.return_value = ([], (16, 16))
        mock_scale_icons.return_value = []

        Game(
            player_service=Mock(spec=PlayerServiceInterface),
            player_id=Mock(spec=PlayerId),
            character_service=Mock(spec=CharacterServiceInterface),
            contract_service=Mock(spec=ContractServiceInterface),
            crafting_service=Mock(spec=CraftingServiceInterface),
            character_id=Mock(spec=CharacterId),
            logging_service=Mock(spec=LoggingServiceInterface),
        )

        mock_scale_icons.assert_called_once_with(
            [], (GFX.active_bar_image_size, GFX.active_bar_image_size)
        )
        mock_active_bar.assert_called_once_with(position=(0, 0), image_list=[])


def test_game_run_loop_quits(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that the main game loop runs, calls its methods, and can be exited."""
    game, mock_player_service, _, _, _, _ = game_with_mocks

    # Configure mock to prevent TypeError in _update
    mock_player_service.get_player_status.return_value = PlayerStatusDTO(
        current_health=100, max_health=100
    )

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


def test_game_quits_on_q_press(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that pressing 'q' sets the is_running flag to False."""
    game, _, _, _, _, _ = game_with_mocks
    assert game.is_running is True

    q_press_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_q})

    with patch("pygame.event.get", return_value=[q_press_event]):
        game._handle_events()

    assert game.is_running is False


def test_game_logs_keypress_in_dev_mode(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that keypresses are logged when dev mode is enabled."""
    game, _, _, _, _, mock_logging_service = game_with_mocks

    with patch("decker_pygame.presentation.game.DEV_SETTINGS.enabled", True):
        key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
        with patch("pygame.event.get", return_value=[key_event]):
            game._handle_events()

    mock_logging_service.log.assert_called_once_with("Key Press", {"key": "a"})


def test_game_update(game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock]):
    """Tests that the _update method calls update on its sprite group."""
    game, mock_player_service, _, _, _, _ = game_with_mocks
    game.all_sprites = Mock()

    # Configure mock to prevent TypeError
    mock_player_service.get_player_status.return_value = PlayerStatusDTO(
        current_health=100, max_health=100
    )

    game._update()

    game.all_sprites.update.assert_called_once()


def test_game_update_calls_update_health(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that the _update method updates the health bar."""
    game, mock_player_service, _, _, _, _ = game_with_mocks
    game.health_bar = Mock(spec=HealthBar)  # Replace real with mock

    # Mock the DTO returned by the service
    from decker_pygame.application.player_service import PlayerStatusDTO

    dto = PlayerStatusDTO(current_health=75, max_health=100)
    mock_player_service.get_player_status.return_value = dto

    game._update()

    mock_player_service.get_player_status.assert_called_once_with(game.player_id)
    game.health_bar.update_health.assert_called_once_with(75, 100)


def test_game_update_no_player_status(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that _update handles the case where the player is not found."""
    game, mock_player_service, _, _, _, _ = game_with_mocks
    game.health_bar = Mock(spec=HealthBar)  # Replace real with mock
    mock_player_service.get_player_status.return_value = None

    game._update()

    # Ensure update_health is not called if there's no status
    mock_player_service.get_player_status.assert_called_once_with(game.player_id)
    game.health_bar.update_health.assert_not_called()


def test_game_show_message(game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock]):
    """Tests that the show_message method calls set_text on the message_view."""
    game, _, _, _, _, _ = game_with_mocks
    # Replace the real view with a mock for this test
    game.message_view = Mock(spec=MessageView)

    game.show_message("Test message")

    game.message_view.set_text.assert_called_once_with("Test message")


def test_game_toggles_build_view(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that pressing 'b' opens and closes the build view."""
    game, _, _, _, mock_crafting_service, _ = game_with_mocks
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
        assert (
            len(game.all_sprites) == 4
        )  # active_bar, alarm_bar, message_view, health_bar


def test_game_toggle_build_view_no_schematics(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock], capsys
):
    """Tests that the build view is not opened if the character has no schematics."""
    game, _, _, _, mock_crafting_service, _ = game_with_mocks
    # Ensure the service returns an empty list
    mock_crafting_service.get_character_schematics.return_value = []

    assert game.build_view is None

    # Press 'b' to attempt to open the view
    open_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_b})
    with patch("pygame.event.get", return_value=[open_event]):
        game._handle_events()

    # View should not be created
    assert game.build_view is None
    assert "No schematics known" in capsys.readouterr().out


def test_game_build_view_event_handling(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that the game correctly delegates events to an active build view."""
    game, _, _, _, _, _ = game_with_mocks
    game.build_view = Mock(spec=BuildView)  # Manually set an active view

    mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})
    with patch("pygame.event.get", return_value=[mouse_event]):
        game._handle_events()

    game.build_view.handle_event.assert_called_once_with(mouse_event)


def test_game_handle_build_click(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests the callback function that handles build clicks."""
    game, _, _, _, mock_crafting_service, _ = game_with_mocks
    schematic_name = "TestSchematic"

    # Spy on the show_message method to verify it's called
    with patch.object(game, "show_message") as spy_show_message:
        # Test success case
        game._handle_build_click(schematic_name)
        mock_crafting_service.craft_item.assert_called_once_with(
            game.character_id, schematic_name
        )
        spy_show_message.assert_called_once_with(
            f"Successfully crafted {schematic_name}!"
        )

        # Test failure case
        mock_crafting_service.craft_item.reset_mock()
        spy_show_message.reset_mock()
        mock_crafting_service.craft_item.side_effect = CraftingError("Test Error")
        game._handle_build_click(schematic_name)
        mock_crafting_service.craft_item.assert_called_once_with(
            game.character_id, schematic_name
        )
        spy_show_message.assert_called_once_with("Crafting failed: Test Error")


def test_game_char_data_view_event_handling(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that the game correctly delegates events to an active
    char data view."""
    game, _, _, _, _, _ = game_with_mocks
    game.char_data_view = Mock(spec=CharDataView)  # Manually set an active view

    mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})
    with patch("pygame.event.get", return_value=[mouse_event]):
        game._handle_events()

    game.char_data_view.handle_event.assert_called_once_with(mouse_event)


def test_game_toggles_char_data_view(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that pressing 'c' opens and closes the character data view."""
    game, mock_player_service, mock_character_service, _, _, _ = game_with_mocks

    # Mock the DTOs returned by the services
    char_dto = CharacterDataDTO(
        name="Testy",
        credits=500,
        reputation=10,
        skills={"hacking": 5},
        unused_skill_points=10,
    )
    mock_character_service.get_character_data.return_value = char_dto

    player_dto = PlayerStatusDTO(current_health=88, max_health=100)
    mock_player_service.get_player_status.return_value = player_dto

    assert game.char_data_view is None

    # Press 'c' to open the view
    open_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c})
    with (
        patch("pygame.event.get", return_value=[open_event]),
        patch("decker_pygame.presentation.game.CharDataView") as mock_view_class,
    ):
        game._handle_events()

        mock_character_service.get_character_data.assert_called_once_with(
            game.character_id
        )
        mock_player_service.get_player_status.assert_called_once_with(game.player_id)

        # Check that the view was instantiated with the correct data
        mock_view_class.assert_called_once_with(
            position=(150, 100),
            size=(400, 450),
            character_name="Testy",
            reputation=10,
            money=500,
            health=88,
            skills={"hacking": 5},
            unused_skill_points=10,
            on_close=game._toggle_char_data_view,
            on_increase_skill=game._on_increase_skill,
            on_decrease_skill=game._on_decrease_skill,
        )
        assert game.char_data_view is mock_view_class.return_value

    # Press 'c' again to close the view
    close_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c})
    with patch("pygame.event.get", return_value=[close_event]):
        game._handle_events()
        assert game.char_data_view is None


def test_toggle_char_data_view_no_data(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock], capsys
):
    """Tests that the char data view is not opened if data is missing."""
    game, mock_player_service, mock_character_service, _, _, _ = game_with_mocks

    # Case 1: Character data is missing
    mock_character_service.get_character_data.return_value = None
    mock_player_service.get_player_status.return_value = PlayerStatusDTO(
        current_health=100, max_health=100
    )

    open_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c})
    with patch("pygame.event.get", return_value=[open_event]):
        game._handle_events()

    # View should not be created
    assert game.char_data_view is None
    assert "Could not retrieve character/player data" in capsys.readouterr().out


def test_game_on_increase_skill(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests the callback for increasing a skill."""
    game, _, mock_character_service, _, _, _ = game_with_mocks

    with patch.object(game, "_toggle_char_data_view") as mock_toggle:
        game._on_increase_skill("hacking")

        mock_character_service.increase_skill.assert_called_once_with(
            game.character_id, "hacking"
        )
        assert mock_toggle.call_count == 2  # Close and re-open


def test_game_on_increase_skill_failure(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests the callback for increasing a skill when the service fails."""
    game, _, mock_character_service, _, _, _ = game_with_mocks
    mock_character_service.increase_skill.side_effect = Exception("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        game._on_increase_skill("hacking")

        mock_show_message.assert_called_once_with("Error: Service Error")


def test_game_on_decrease_skill(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests the callback for decreasing a skill."""
    game, _, mock_character_service, _, _, _ = game_with_mocks

    with patch.object(game, "_toggle_char_data_view") as mock_toggle:
        game._on_decrease_skill("hacking")

        mock_character_service.decrease_skill.assert_called_once_with(
            game.character_id, "hacking"
        )
        assert mock_toggle.call_count == 2  # Close and re-open


def test_game_toggles_contract_list_view(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that pressing 'l' opens and closes the contract list view."""
    game, _, _, _, _, _ = game_with_mocks

    assert game.contract_list_view is None

    # Press 'l' to open the view
    open_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_l})
    with (
        patch("pygame.event.get", return_value=[open_event]),
        patch("decker_pygame.presentation.game.ContractListView") as mock_view_class,
    ):
        game._handle_events()
        mock_view_class.assert_called_once()
        assert game.contract_list_view is not None

    # Press 'l' again to close the view
    close_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_l})
    with patch("pygame.event.get", return_value=[close_event]):
        game._handle_events()
        assert game.contract_list_view is None


def test_game_toggles_contract_data_view(
    game_with_mocks: tuple[Game, Mock, Mock, Mock, Mock, Mock],
):
    """Tests that pressing 'd' opens and closes the contract data view."""
    game, _, _, _, _, _ = game_with_mocks

    assert game.contract_data_view is None

    # Press 'd' to open the view
    open_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d})
    with (
        patch("pygame.event.get", return_value=[open_event]),
        patch("decker_pygame.presentation.game.ContractDataView") as mock_view_class,
    ):
        game._handle_events()
        mock_view_class.assert_called_once()
        assert game.contract_data_view is not None

    # Press 'd' again to close the view
    close_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d})
    with patch("pygame.event.get", return_value=[close_event]):
        game._handle_events()
        assert game.contract_data_view is None
