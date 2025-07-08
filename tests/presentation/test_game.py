import uuid
from collections.abc import Generator
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.character_service import (
    CharacterDataDTO,
    CharacterViewData,
)
from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.application.deck_service import DeckViewData
from decker_pygame.application.player_service import PlayerStatusDTO
from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    DeckServiceInterface,
    LoggingServiceInterface,
    PlayerServiceInterface,
)
from decker_pygame.presentation.components.build_view import BuildView
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


@dataclass
class Mocks:
    """A container for all mocked objects used in game tests."""

    game: Game
    player_service: Mock
    character_service: Mock
    contract_service: Mock
    crafting_service: Mock
    deck_service: Mock
    logging_service: Mock


@pytest.fixture
def game_with_mocks() -> Generator[Mocks]:
    """
    Provides a fully mocked Game instance and its mocked dependencies.
    """
    mock_player_service = Mock(spec=PlayerServiceInterface)
    mock_character_service = Mock(spec=CharacterServiceInterface)
    mock_contract_service = Mock(spec=ContractServiceInterface)
    mock_crafting_service = Mock(spec=CraftingServiceInterface)
    mock_deck_service = Mock(spec=DeckServiceInterface)
    mock_logging_service = Mock(spec=LoggingServiceInterface)
    dummy_player_id = PlayerId(uuid.uuid4())
    dummy_character_id = CharacterId(uuid.uuid4())

    # Mock all external dependencies called in Game.__init__ and Game.run
    with (
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.display.flip"),
        patch("pygame.time.Clock"),
        patch("decker_pygame.presentation.game.PygameInputHandler"),
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
            deck_service=mock_deck_service,
            character_id=dummy_character_id,
            logging_service=mock_logging_service,
        )
        mock_scale_icons.return_value = [pygame.Surface((32, 32))]
        yield Mocks(
            game=game,
            player_service=mock_player_service,
            character_service=mock_character_service,
            contract_service=mock_contract_service,
            crafting_service=mock_crafting_service,
            deck_service=mock_deck_service,
            logging_service=mock_logging_service,
        )


def test_game_initialization(game_with_mocks: Mocks):
    """Tests that the Game class correctly stores its injected dependencies."""
    mocks = game_with_mocks
    game = mocks.game

    # The __init__ method should store the service and id
    assert game.player_service is mocks.player_service
    assert game.character_service is mocks.character_service
    assert game.contract_service is mocks.contract_service
    assert game.crafting_service is mocks.crafting_service
    assert game.deck_service is mocks.deck_service
    assert game.logging_service is mocks.logging_service
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
        patch("decker_pygame.presentation.game.PygameInputHandler"),
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
            deck_service=Mock(spec=DeckServiceInterface),
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
        patch("decker_pygame.presentation.game.PygameInputHandler"),
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
            deck_service=Mock(spec=DeckServiceInterface),
            character_id=Mock(spec=CharacterId),
            logging_service=Mock(spec=LoggingServiceInterface),
        )

        mock_scale_icons.assert_called_once_with(
            [], (GFX.active_bar_image_size, GFX.active_bar_image_size)
        )
        mock_active_bar.assert_called_once_with(position=(0, 0), image_list=[])


def test_game_run_loop_quits(game_with_mocks: Mocks):
    """Tests that the main game loop runs, calls its methods, and can be exited."""
    mocks = game_with_mocks
    game = mocks.game

    # Configure mock to prevent TypeError in _update
    mocks.player_service.get_player_status.return_value = PlayerStatusDTO(
        current_health=100, max_health=100
    )

    # This function will be the side_effect for the mock input handler.
    # It allows us to control the game loop from outside for the test.
    def quit_on_second_call(*args, **kwargs):
        # The mock's own call_count tells us which iteration we are on.
        if game.input_handler.handle_events.call_count == 2:  # type: ignore[attribute-error]
            game.quit()

    game.input_handler.handle_events.side_effect = quit_on_second_call  # type: ignore[attribute-error]

    with patch("pygame.quit") as mock_pygame_quit:
        game.run()

    # The loop should have run twice before quitting
    assert game.input_handler.handle_events.call_count == 2  # type: ignore[attribute-error]
    assert game.clock.tick.call_count == 2  # type: ignore[attribute-error]
    # The final pygame.quit() should be called
    mock_pygame_quit.assert_called_once()


def test_game_quit_method(game_with_mocks: Mocks):
    """Tests that the public quit() method sets the is_running flag to False."""
    game = game_with_mocks.game
    assert game.is_running is True
    game.quit()
    assert game.is_running is False


def test_game_update(game_with_mocks: Mocks):
    """Tests that the _update method calls update on its sprite group."""
    mocks = game_with_mocks
    game = mocks.game
    game.all_sprites = Mock()

    # Configure mock to prevent TypeError
    mocks.player_service.get_player_status.return_value = PlayerStatusDTO(
        current_health=100, max_health=100
    )

    game._update()

    game.all_sprites.update.assert_called_once()


def test_game_update_calls_update_health(game_with_mocks: Mocks):
    """Tests that the _update method updates the health bar."""
    mocks = game_with_mocks
    game = mocks.game
    game.health_bar = Mock(spec=HealthBar)  # Replace real with mock

    dto = PlayerStatusDTO(current_health=75, max_health=100)
    mocks.player_service.get_player_status.return_value = dto

    game._update()

    mocks.player_service.get_player_status.assert_called_once_with(game.player_id)
    game.health_bar.update_health.assert_called_once_with(75, 100)


def test_game_update_no_player_status(game_with_mocks: Mocks):
    """Tests that _update handles the case where the player is not found."""
    mocks = game_with_mocks
    game = mocks.game
    game.health_bar = Mock(spec=HealthBar)  # Replace real with mock
    mocks.player_service.get_player_status.return_value = None

    game._update()

    # Ensure update_health is not called if there's no status
    mocks.player_service.get_player_status.assert_called_once_with(game.player_id)
    game.health_bar.update_health.assert_not_called()


def test_game_show_message(game_with_mocks: Mocks):
    """Tests that the show_message method calls set_text on the message_view."""
    game = game_with_mocks.game
    # Replace the real view with a mock for this test
    game.message_view = Mock(spec=MessageView)

    game.show_message("Test message")

    game.message_view.set_text.assert_called_once_with("Test message")


def test_game_toggles_build_view(game_with_mocks: Mocks):
    """Tests that the toggle_build_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game
    # Ensure the service returns schematics so the view can be created
    mocks.crafting_service.get_character_schematics.return_value = [Mock()]

    assert game.build_view is None

    # Call the public method to open the view
    with patch(
        "decker_pygame.presentation.game.BuildView", spec=BuildView
    ) as mock_build_view_class:
        game.toggle_build_view()
        mock_build_view_class.assert_called_once()
        assert game.build_view is not None
        assert game.build_view in game.all_sprites

    # Call again to close the view
    game.toggle_build_view()
    assert game.build_view is None
    # Check that the sprite was removed from the group
    assert len(game.all_sprites) == 4


def test_game_toggle_build_view_no_schematics(game_with_mocks: Mocks, capsys):
    """Tests that the build view is not opened if the character has no schematics."""
    mocks = game_with_mocks
    game = mocks.game
    # Ensure the service returns an empty list
    mocks.crafting_service.get_character_schematics.return_value = []

    assert game.build_view is None

    # Call the public method
    game.toggle_build_view()

    assert game.build_view is None  # View should not be created
    assert "No schematics known" in capsys.readouterr().out


def test_game_handle_build_click(game_with_mocks: Mocks):
    """Tests the callback function that handles build clicks."""
    mocks = game_with_mocks
    game = mocks.game
    schematic_name = "TestSchematic"

    # Spy on the show_message method to verify it's called
    with patch.object(game, "show_message") as spy_show_message:
        # Test success case
        game._handle_build_click(schematic_name)
        mocks.crafting_service.craft_item.assert_called_once_with(
            game.character_id, schematic_name
        )
        spy_show_message.assert_called_once_with(
            f"Successfully crafted {schematic_name}!"
        )

        # Test failure case
        mocks.crafting_service.craft_item.reset_mock()
        spy_show_message.reset_mock()
        mocks.crafting_service.craft_item.side_effect = CraftingError("Test Error")
        game._handle_build_click(schematic_name)
        mocks.crafting_service.craft_item.assert_called_once_with(
            game.character_id, schematic_name
        )
        spy_show_message.assert_called_once_with("Crafting failed: Test Error")


def test_game_toggles_char_data_view(game_with_mocks: Mocks):
    """Tests that the toggle_char_data_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game

    # Mock the aggregated View Model DTO from the character service
    view_data = CharacterViewData(
        name="Testy",
        credits=500,
        reputation=10,
        skills={"hacking": 5},
        unused_skill_points=10,
        health=88,
    )
    mocks.character_service.get_character_view_data.return_value = view_data

    assert game.char_data_view is None

    # Call the public method to open the view
    with patch("decker_pygame.presentation.game.CharDataView") as mock_view_class:
        game.toggle_char_data_view()

        # Check that the view was instantiated with the correct data
        mock_view_class.assert_called_once_with(
            position=(150, 100),
            data=view_data,
            on_close=game.toggle_char_data_view,
            on_increase_skill=game._on_increase_skill,
            on_decrease_skill=game._on_decrease_skill,
        )
        assert game.char_data_view is mock_view_class.return_value

    # Call again to close the view
    game.toggle_char_data_view()
    assert game.char_data_view is None


def test_toggle_char_data_view_no_data(game_with_mocks: Mocks, capsys):
    """Tests that the char data view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game

    # Simulate the service returning no data
    mocks.character_service.get_character_view_data.return_value = None

    # Call the public method
    game.toggle_char_data_view()
    # View should not be created
    assert game.char_data_view is None
    assert "Could not retrieve character/player data" in capsys.readouterr().out


def test_game_on_increase_skill(game_with_mocks: Mocks):
    """Tests the callback for increasing a skill."""
    mocks = game_with_mocks
    game = mocks.game

    with patch.object(game, "toggle_char_data_view") as mock_toggle:
        game._on_increase_skill("hacking")

        mocks.character_service.increase_skill.assert_called_once_with(
            game.character_id, "hacking"
        )
        assert mock_toggle.call_count == 2  # Close and re-open


def test_game_on_increase_skill_failure(game_with_mocks: Mocks):
    """Tests the callback for increasing a skill when the service fails."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.character_service.increase_skill.side_effect = Exception("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        game._on_increase_skill("hacking")

        mock_show_message.assert_called_once_with("Error: Service Error")


def test_game_on_decrease_skill(game_with_mocks: Mocks):
    """Tests the callback for decreasing a skill."""
    mocks = game_with_mocks
    game = mocks.game

    with patch.object(game, "toggle_char_data_view") as mock_toggle:
        game._on_decrease_skill("hacking")

        mocks.character_service.decrease_skill.assert_called_once_with(
            game.character_id, "hacking"
        )
        assert mock_toggle.call_count == 2  # Close and re-open


def test_game_toggles_contract_list_view(game_with_mocks: Mocks):
    """Tests that the toggle_contract_list_view method opens and closes the view."""
    game = game_with_mocks.game

    assert game.contract_list_view is None

    # Call the public method to open the view
    with patch("decker_pygame.presentation.game.ContractListView") as mock_view_class:
        game.toggle_contract_list_view()
        mock_view_class.assert_called_once()
        assert game.contract_list_view is not None

    # Call again to close the view
    game.toggle_contract_list_view()
    assert game.contract_list_view is None


def test_game_toggles_contract_data_view(game_with_mocks: Mocks):
    """Tests that the toggle_contract_data_view method opens and closes the view."""
    game = game_with_mocks.game

    assert game.contract_data_view is None

    # Call the public method to open the view
    with patch("decker_pygame.presentation.game.ContractDataView") as mock_view_class:
        game.toggle_contract_data_view()
        mock_view_class.assert_called_once()
        assert game.contract_data_view is not None

    # Call again to close the view
    game.toggle_contract_data_view()
    assert game.contract_data_view is None


def test_game_toggles_deck_view(game_with_mocks: Mocks):
    """Tests that the toggle_deck_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game

    # Mock the DTOs returned by the services
    mock_deck_id = DeckId(uuid.uuid4())
    char_dto = CharacterDataDTO(
        name="Testy",
        credits=500,
        skills={},
        unused_skill_points=0,
        deck_id=mock_deck_id,
    )
    mocks.character_service.get_character_data.return_value = char_dto

    deck_data = DeckViewData(programs=[])
    mocks.deck_service.get_deck_view_data.return_value = deck_data

    assert game.deck_view is None

    # Call the public method to open the view
    with patch("decker_pygame.presentation.game.DeckView") as mock_view_class:
        game.toggle_deck_view()

        # Assert that the correct services were called
        mocks.character_service.get_character_data.assert_called_once_with(
            game.character_id
        )
        mocks.deck_service.get_deck_view_data.assert_called_once_with(mock_deck_id)

        # Check that the view was instantiated with the correct data
        mock_view_class.assert_called_once_with(
            data=deck_data, on_close=game.toggle_deck_view
        )
        assert game.deck_view is mock_view_class.return_value

    # Call again to close the view
    game.toggle_deck_view()
    assert game.deck_view is None


def test_toggle_deck_view_no_data(game_with_mocks: Mocks, capsys):
    """Tests that the deck view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game

    # Case 1: Character data is missing
    mocks.character_service.get_character_data.return_value = None
    game.toggle_deck_view()
    assert game.deck_view is None
    assert "Could not retrieve character data" in capsys.readouterr().out

    # Case 2: Deck data is missing
    # We need to configure the mock DTO to have a deck_id for the service call
    mock_char_data = Mock(spec=CharacterDataDTO)
    mock_char_data.deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = mock_char_data
    mocks.deck_service.get_deck_view_data.return_value = None
    game.toggle_deck_view()
    assert game.deck_view is None
    assert "Could not retrieve deck data" in capsys.readouterr().out
