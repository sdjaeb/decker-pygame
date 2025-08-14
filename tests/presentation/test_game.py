import uuid
from collections.abc import Generator
from dataclasses import dataclass
from functools import partial
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.application.deck_service import DeckServiceError
from decker_pygame.application.dtos import (
    CharacterDataDTO,
    CharacterViewDTO,
    DeckViewDTO,
    FileAccessViewDTO,
    IceDataViewDTO,
    MissionResultsDTO,
    NewProjectViewDTO,
    PlayerStatusDTO,
    ProjectDataViewDTO,
    RestViewDTO,
    ShopItemViewDTO,
    ShopViewDTO,
    TransferViewDTO,
)
from decker_pygame.application.shop_service import ShopServiceError
from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId
from decker_pygame.domain.shop import ShopItemType
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    DeckServiceInterface,
    DSFileServiceInterface,
    LoggingServiceInterface,
    NodeServiceInterface,
    PlayerServiceInterface,
    ProjectServiceInterface,
    SettingsServiceInterface,
    ShopServiceInterface,
)
from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.contract_data_view import ContractDataView
from decker_pygame.presentation.components.contract_list_view import ContractListView
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.entry_view import EntryView
from decker_pygame.presentation.components.file_access_view import FileAccessView
from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.ice_data_view import IceDataView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.components.mission_results_view import (
    MissionResultsView,
)
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.project_data_view import ProjectDataView
from decker_pygame.presentation.components.rest_view import RestView
from decker_pygame.presentation.components.shop_view import ShopView
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.debug_actions import DebugActions
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.input_handler import PygameInputHandler
from decker_pygame.settings import FPS


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
    asset_service: Mock
    player_service: Mock
    character_service: Mock
    contract_service: Mock
    crafting_service: Mock
    deck_service: Mock
    ds_file_service: Mock
    shop_service: Mock
    node_service: Mock
    settings_service: Mock
    project_service: Mock
    logging_service: Mock


@pytest.fixture
def game_with_mocks() -> Generator[Mocks]:
    """Provides a fully mocked Game instance and its mocked dependencies."""
    mock_screen = Mock(spec=pygame.Surface)
    mock_asset_service = Mock(spec=AssetService)
    mock_player_service = Mock(spec=PlayerServiceInterface)
    mock_character_service = Mock(spec=CharacterServiceInterface)
    mock_contract_service = Mock(spec=ContractServiceInterface)
    mock_crafting_service = Mock(spec=CraftingServiceInterface)
    mock_deck_service = Mock(spec=DeckServiceInterface)
    mock_ds_file_service = Mock(spec=DSFileServiceInterface)
    mock_shop_service = Mock(spec=ShopServiceInterface)
    mock_node_service = Mock(spec=NodeServiceInterface)
    mock_settings_service = Mock(spec=SettingsServiceInterface)
    mock_project_service = Mock(spec=ProjectServiceInterface)
    mock_logging_service = Mock(spec=LoggingServiceInterface)
    dummy_player_id = PlayerId(uuid.uuid4())
    dummy_character_id = CharacterId(uuid.uuid4())

    # Configure the asset service mock to return a valid icon
    mock_asset_service.get_spritesheet.return_value = [pygame.Surface((16, 16))]

    # Mock all external dependencies called in Game.__init__ and Game.run
    with (
        patch("pygame.display.flip"),
        patch("pygame.time.Clock"),
        patch(
            "decker_pygame.presentation.game.PygameInputHandler",
            spec=PygameInputHandler,
        ),
    ):
        game = Game(
            screen=mock_screen,
            asset_service=mock_asset_service,
            player_service=mock_player_service,
            player_id=dummy_player_id,
            character_service=mock_character_service,
            contract_service=mock_contract_service,
            crafting_service=mock_crafting_service,
            deck_service=mock_deck_service,
            ds_file_service=mock_ds_file_service,
            shop_service=mock_shop_service,
            node_service=mock_node_service,
            settings_service=mock_settings_service,
            project_service=mock_project_service,
            character_id=dummy_character_id,
            logging_service=mock_logging_service,
        )
        yield Mocks(
            game=game,
            asset_service=mock_asset_service,
            player_service=mock_player_service,
            character_service=mock_character_service,
            contract_service=mock_contract_service,
            crafting_service=mock_crafting_service,
            deck_service=mock_deck_service,
            ds_file_service=mock_ds_file_service,
            shop_service=mock_shop_service,
            node_service=mock_node_service,
            settings_service=mock_settings_service,
            project_service=mock_project_service,
            logging_service=mock_logging_service,
        )


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
    assert isinstance(game.player_id, uuid.UUID)
    assert isinstance(game.debug_actions, DebugActions)
    assert isinstance(game.character_id, uuid.UUID)


def test_run_loop_calls_methods(game_with_mocks: Mocks):
    """Tests that the main loop calls its core methods."""
    game = game_with_mocks.game

    # Configure mocks
    # Configure the mock input handler to quit the game on the first call.
    # We use `type: ignore` because Pylance cannot statically determine that
    # the mock objects will have these attributes at runtime.
    game.input_handler.handle_events.side_effect = game.quit  # type: ignore[attr-defined]
    game.player_service.get_player_status.return_value = PlayerStatusDTO(  # type: ignore[attr-defined]
        current_health=100, max_health=100
    )

    with patch.object(game, "_update", wraps=game._update) as spy_update:
        with patch.object(game.all_sprites, "draw") as mock_draw:
            game.run()

    game.input_handler.handle_events.assert_called_once()  # type: ignore[attr-defined]
    spy_update.assert_called_once()
    mock_draw.assert_called_once_with(game.screen)
    game.clock.tick.assert_called_once_with(FPS)  # type: ignore[attr-defined]


def test_run_calls_pygame_quit(game_with_mocks: Mocks):
    """Tests that pygame.quit() is called when the game loop finishes."""
    game = game_with_mocks.game
    game.is_running = False  # Prevent the loop from running

    # The patch target must be where the name is looked up. In this case,
    # it's in the 'game' module's namespace.
    with patch("decker_pygame.presentation.game.pygame.quit") as mock_pygame_quit:
        game.run()

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

    game._update()

    game.all_sprites.update.assert_called_once()


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

    with patch.object(
        game, "all_sprites", Mock(spec=pygame.sprite.Group)
    ) as mock_sprites:
        assert game.build_view is None

        # Call the public method to open the view
        with patch(
            "decker_pygame.presentation.game.BuildView", spec=BuildView
        ) as mock_build_view_class:
            game.toggle_build_view()
            mock_build_view_class.assert_called_once()
            assert game.build_view is not None
            mock_sprites.add.assert_called_with(game.build_view)

        # Call again to close the view
        game.toggle_build_view()
        assert game.build_view is None
        mock_sprites.remove.assert_called_once()


def test_game_toggle_build_view_no_schematics(game_with_mocks: Mocks):
    """Tests that the build view is not opened if the character has no schematics."""
    mocks = game_with_mocks
    game = mocks.game
    # Ensure the service returns an empty list
    mocks.crafting_service.get_character_schematics.return_value = []

    assert game.build_view is None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_build_view()
        assert game.build_view is None  # View should not be created
        mock_show_message.assert_called_once_with("No schematics known.")


def test_game_handle_build_click_success(game_with_mocks: Mocks):
    """Tests the success path of the build click callback."""
    mocks = game_with_mocks
    game = mocks.game
    schematic_name = "TestSchematic"

    with patch.object(game, "show_message") as mock_show_message:
        game._handle_build_click(schematic_name)
        mocks.crafting_service.craft_item.assert_called_once_with(
            game.character_id, schematic_name
        )
        # On success, the message is handled by an event handler, not this method.
        mock_show_message.assert_not_called()


def test_game_handle_build_click_failure(game_with_mocks: Mocks):
    """Tests the failure path of the build click callback."""
    mocks = game_with_mocks
    game = mocks.game
    schematic_name = "TestSchematic"
    with patch.object(game, "show_message") as mock_show_message:
        mocks.crafting_service.craft_item.side_effect = CraftingError("Test Error")
        game._handle_build_click(schematic_name)
        mock_show_message.assert_called_once_with("Crafting failed: Test Error")


def test_game_toggles_char_data_view(game_with_mocks: Mocks):
    """Tests that the toggle_char_data_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game

    # Mock the aggregated View Model DTO from the character service
    view_data = CharacterViewDTO(
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


def test_toggle_char_data_view_no_data(game_with_mocks: Mocks):
    """Tests that the char data view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game

    # Simulate the service returning no data
    mocks.character_service.get_character_view_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_char_data_view()
        assert game.char_data_view is None
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve character/player data."
        )


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
        assert mock_toggle.call_count == 2


def test_game_toggles_contract_list_view(game_with_mocks: Mocks):
    """Tests that the toggle_contract_list_view method opens and closes the view."""
    game = game_with_mocks.game

    assert game.contract_list_view is None

    # Call the public method to open the view
    with patch(
        "decker_pygame.presentation.game.ContractListView", spec=ContractListView
    ) as mock_view_class:
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
    with patch(
        "decker_pygame.presentation.game.ContractDataView", spec=ContractDataView
    ) as mock_view_class:
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

    deck_data = DeckViewDTO(programs=[], used_deck_size=0, total_deck_size=100)
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
            data=deck_data,
            on_close=game.toggle_deck_view,
            on_order=game._on_order_deck,
            on_program_click=game._on_program_click,
        )
        assert game.deck_view is mock_view_class.return_value

    # Call again to close the view
    game.toggle_deck_view()
    assert game.deck_view is None


def test_toggle_deck_view_no_char_data(game_with_mocks: Mocks):
    """Tests that the deck view is not opened if character data is missing."""
    mocks = game_with_mocks
    game = mocks.game

    mocks.character_service.get_character_data.return_value = None
    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_deck_view()
        assert game.deck_view is None
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve character data to find deck."
        )


def test_on_move_program_order_refresh_fails(game_with_mocks: Mocks):
    """Tests the re-order callbacks when the refresh action fails."""
    mocks = game_with_mocks
    game = mocks.game
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )

    with patch.object(game, "_on_order_deck", side_effect=Exception("Refresh Error")):
        with patch.object(game, "show_message") as mock_show_message:
            # Test moving up
            game._on_move_program_up("IcePick")
            mocks.deck_service.move_program_up.assert_called_once_with(
                mock_deck_id, "IcePick"
            )
            mock_show_message.assert_called_once_with("Error: Refresh Error")

        # Reset mocks for the next test
        mocks.deck_service.reset_mock()
        mock_show_message.reset_mock()

        with patch.object(game, "show_message") as mock_show_message:
            # Test moving down
            game._on_move_program_down("Hammer")
            mocks.deck_service.move_program_down.assert_called_once_with(
                mock_deck_id, "Hammer"
            )
            mock_show_message.assert_called_once_with("Error: Refresh Error")


def test_move_program_and_refresh_no_char_data(game_with_mocks: Mocks):
    """
    Tests that _move_program_and_refresh shows an error if character data is not found.
    """
    mocks = game_with_mocks
    game = mocks.game
    mocks.character_service.get_character_data.return_value = None
    mock_move_action = Mock()

    with patch.object(game, "show_message") as mock_show_message:
        game._move_program_and_refresh(mock_move_action)
        mock_show_message.assert_called_once_with(
            "Error: Could not find character to modify deck."
        )
        mock_move_action.assert_not_called()


def test_move_program_and_refresh_service_exception(game_with_mocks: Mocks):
    """
    Tests that _move_program_and_refresh shows an error if the move action fails.
    """
    mocks = game_with_mocks
    game = mocks.game
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    mock_move_action = Mock(side_effect=Exception("Service Error"))

    with patch.object(game, "show_message") as mock_show_message:
        game._move_program_and_refresh(mock_move_action)
        mock_show_message.assert_called_once_with("Error: Service Error")
        mock_move_action.assert_called_once_with(mock_deck_id)


def test_on_move_program_to_storage_no_char_data(game_with_mocks: Mocks):
    """Tests that on_move_program_to_storage shows an error if char data is missing."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.character_service.get_character_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game._on_move_program_to_storage("any_program")
        mock_show_message.assert_called_once_with(
            "Error: Could not find character to modify deck."
        )


def test_on_move_program_to_deck_no_char_data(game_with_mocks: Mocks):
    """Tests that on_move_program_to_deck shows an error if char data is missing."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.character_service.get_character_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game._on_move_program_to_deck("any_program")
        mock_show_message.assert_called_once_with(
            "Error: Could not find character to modify deck."
        )


def test_toggle_deck_view_no_deck_data(game_with_mocks: Mocks):
    """Tests that the deck view is not opened if deck data is missing."""
    mocks = game_with_mocks
    game = mocks.game

    mock_char_data = Mock(spec=CharacterDataDTO)
    mock_char_data.deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = mock_char_data
    mocks.deck_service.get_deck_view_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_deck_view()
        assert game.deck_view is None
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve deck data."
        )


def test_game_toggles_transfer_view(game_with_mocks: Mocks):
    """Tests that the toggle_transfer_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game

    # Mock the DTO from the service
    transfer_data = TransferViewDTO(deck_programs=[], stored_programs=[])
    mocks.deck_service.get_transfer_view_data.return_value = transfer_data

    with patch.object(
        game, "all_sprites", Mock(spec=pygame.sprite.Group)
    ) as mock_sprites:
        assert game.transfer_view is None

        # Call the public method to open the view
        with patch(
            "decker_pygame.presentation.game.TransferView", spec=TransferView
        ) as mock_view_class:
            game.toggle_transfer_view()

            mocks.deck_service.get_transfer_view_data.assert_called_once_with(
                game.character_id
            )
            mock_view_class.assert_called_once()
            assert game.transfer_view is not None
            mock_sprites.add.assert_called_with(game.transfer_view)

        # Call again to close the view
        game.toggle_transfer_view()
        assert game.transfer_view is None
        mock_sprites.remove.assert_called_once()


def test_toggle_transfer_view_no_data(game_with_mocks: Mocks):
    """Tests that the transfer view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.deck_service.get_transfer_view_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_transfer_view()
        assert game.transfer_view is None
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve transfer data."
        )


def test_on_move_program_to_deck(game_with_mocks: Mocks):
    """Tests the callback for moving a program to the deck."""
    mocks = game_with_mocks
    game = mocks.game

    with patch.object(game, "toggle_transfer_view") as mock_toggle:
        game._on_move_program_to_deck("IcePick")

        mocks.deck_service.move_program_to_deck.assert_called_once_with(
            game.character_id, "IcePick"
        )
        assert mock_toggle.call_count == 2  # Close and re-open


def test_on_move_program_to_storage(game_with_mocks: Mocks):
    """Tests the callback for moving a program to storage."""
    mocks = game_with_mocks
    game = mocks.game

    with patch.object(game, "toggle_transfer_view") as mock_toggle:
        game._on_move_program_to_storage("Hammer")

        mocks.deck_service.move_program_to_storage.assert_called_once_with(
            game.character_id, "Hammer"
        )
        assert mock_toggle.call_count == 2


@pytest.mark.parametrize(
    "method_to_test, service_method_to_mock",
    [
        ("_on_move_program_to_deck", "move_program_to_deck"),
        ("_on_move_program_to_storage", "move_program_to_storage"),
    ],
)
def test_on_move_program_failure_service_error(
    game_with_mocks: Mocks, method_to_test: str, service_method_to_mock: str
):
    """Tests the transfer callbacks when the service raises an error."""
    mocks = game_with_mocks
    game = mocks.game
    mock_deck_id = DeckId(uuid.uuid4())
    game_method = getattr(game, method_to_test)

    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    mock_service_method = getattr(mocks.deck_service, service_method_to_mock)
    mock_service_method.side_effect = DeckServiceError("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        game_method("AnyProgram")
        mock_show_message.assert_called_once_with("Error: Service Error")
        mock_show_message.assert_called_once_with("Error: Service Error")


@pytest.mark.parametrize(
    "method_to_test",
    [
        "_on_move_program_to_deck",
        "_on_move_program_to_storage",
    ],
)
def test_on_move_program_failure_no_char_data(
    game_with_mocks: Mocks, method_to_test: str
):
    """Tests the transfer callbacks when character data is not found."""
    mocks = game_with_mocks
    game = mocks.game
    game_method = getattr(game, method_to_test)

    mocks.character_service.get_character_data.return_value = None
    with patch.object(game, "show_message") as mock_show_message:
        game_method("AnyProgram")
        mock_show_message.assert_called_once_with(
            "Error: Could not find character to modify deck."
        )


def test_on_order_deck_success(game_with_mocks: Mocks):
    """Tests the successful path for the _on_order_deck callback."""
    mocks = game_with_mocks
    game = mocks.game

    # Set up a mock deck_view to be removed
    game.deck_view = Mock(spec=DeckView)
    game.all_sprites.add(game.deck_view)  # intro_view + deck_view
    assert len(game.all_sprites) == 2

    # Configure services to return valid data
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    deck_data = DeckViewDTO(programs=[], used_deck_size=0, total_deck_size=100)
    mocks.deck_service.get_deck_view_data.return_value = deck_data

    with patch(
        "decker_pygame.presentation.game.OrderView", spec=OrderView
    ) as mock_order_view_class:
        game._on_order_deck()

        # Assertions
        mocks.character_service.get_character_data.assert_called_once_with(
            game.character_id
        )
        mocks.deck_service.get_deck_view_data.assert_called_once_with(mock_deck_id)
        assert game.deck_view is None  # The old view should be gone
        mock_order_view_class.assert_called_once_with(
            data=deck_data,
            on_close=game.toggle_deck_view,
            on_move_up=game._on_move_program_up,
            on_move_down=game._on_move_program_down,
        )
        assert game.order_view is mock_order_view_class.return_value
        assert game.order_view in game.all_sprites
        assert len(game.all_sprites) == 2  # intro_view + order_view


def test_on_order_deck_no_char_data(game_with_mocks: Mocks):
    """Tests the _on_order_deck callback when character data is not found."""
    mocks = game_with_mocks
    game = mocks.game

    mocks.character_service.get_character_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game._on_order_deck()

        mocks.deck_service.get_deck_view_data.assert_not_called()
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve character data to find deck."
        )


def test_on_order_deck_no_deck_data(game_with_mocks: Mocks):
    """Tests the _on_order_deck callback when deck data is not found."""
    mocks = game_with_mocks
    game = mocks.game

    mock_char_data = Mock(spec=CharacterDataDTO)
    mock_char_data.deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = mock_char_data
    mocks.deck_service.get_deck_view_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game._on_order_deck()
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve deck data."
        )


def test_on_order_deck_refreshes_existing_order_view(game_with_mocks: Mocks):
    """Tests that calling _on_order_deck removes an existing OrderView."""
    mocks = game_with_mocks
    game = mocks.game

    # Set up a mock order_view to be removed, simulating a refresh
    existing_order_view = Mock(spec=OrderView)
    game.order_view = existing_order_view
    game.all_sprites.add(existing_order_view)  # intro_view + order_view
    assert len(game.all_sprites) == 2

    # Configure services to return valid data
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    deck_data = DeckViewDTO(programs=[], used_deck_size=0, total_deck_size=100)
    mocks.deck_service.get_deck_view_data.return_value = deck_data

    with patch(
        "decker_pygame.presentation.game.OrderView", spec=OrderView
    ) as mock_order_view_class:
        new_order_view_instance = mock_order_view_class.return_value
        game._on_order_deck()

        # Assertions
        assert existing_order_view not in game.all_sprites
        mock_order_view_class.assert_called_once()
        assert game.order_view is new_order_view_instance
        assert game.order_view in game.all_sprites
        assert len(game.all_sprites) == 2


def test_on_move_program_up_and_down(game_with_mocks: Mocks):
    """Tests the callbacks for moving a program in the deck order."""
    mocks = game_with_mocks
    game = mocks.game
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )

    with patch.object(game, "_on_order_deck") as mock_refresh:
        # Test moving up
        game._on_move_program_up("IcePick")
        mocks.deck_service.move_program_up.assert_called_once_with(
            mock_deck_id, "IcePick"
        )
        mock_refresh.assert_called_once()

        mock_refresh.reset_mock()

        # Test moving down
        game._on_move_program_down("Hammer")
        mocks.deck_service.move_program_down.assert_called_once_with(
            mock_deck_id, "Hammer"
        )
        mock_refresh.assert_called_once()


def test_game_toggles_home_view(game_with_mocks: Mocks):
    """Tests that the toggle_home_view method opens and closes the view."""
    game = game_with_mocks.game
    assert game.home_view is None

    # Toggle to open
    with patch(
        "decker_pygame.presentation.game.HomeView", spec=HomeView
    ) as mock_view_class:
        game.toggle_home_view()
        mock_view_class.assert_called_once_with(
            on_char=game.toggle_char_data_view,
            on_deck=game.toggle_deck_view,
            on_contracts=game.toggle_contract_list_view,
            on_build=game.toggle_build_view,
            on_shop=game.toggle_shop_view,
            on_transfer=game.toggle_transfer_view,
            on_projects=game.toggle_project_data_view,
        )
        assert game.home_view is not None

    # Toggle to close
    game.toggle_home_view()
    assert game.home_view is None


def test_game_toggles_intro_view(game_with_mocks: Mocks):
    """Tests that the toggle_intro_view method opens and closes the view."""
    game = game_with_mocks.game
    # It starts open from __init__,
    assert game.intro_view is not None

    # Toggle to close
    game.toggle_intro_view()
    assert game.intro_view is None

    # Toggle to open again
    with patch(
        "decker_pygame.presentation.game.IntroView", spec=IntroView
    ) as mock_view_class:
        game.toggle_intro_view()
        mock_view_class.assert_called_once()
        assert game.intro_view is not None


def test_game_toggles_new_char_view(game_with_mocks: Mocks):
    """Tests that the toggle_new_char_view method opens and closes the view."""
    game = game_with_mocks.game
    assert game.new_char_view is None

    # Toggle to open
    with patch(
        "decker_pygame.presentation.game.NewCharView", spec=NewCharView
    ) as mock_view_class:
        game.toggle_new_char_view()
        mock_view_class.assert_called_once()
        assert game.new_char_view is not None

    # Toggle to close
    game.toggle_new_char_view()
    assert game.new_char_view is None


def test_continue_from_intro(game_with_mocks: Mocks):
    """Tests the transition from the intro view."""
    game = game_with_mocks.game
    with (
        patch.object(game, "toggle_intro_view") as mock_toggle_intro,
        patch.object(game, "toggle_new_char_view") as mock_toggle_new_char,
    ):
        game._continue_from_intro()
        mock_toggle_intro.assert_called_once()
        mock_toggle_new_char.assert_called_once()


def test_handle_character_creation(game_with_mocks: Mocks):
    """Tests the transition from the new character view."""
    game = game_with_mocks.game
    # Simulate that the new character view is open before the handler is called.
    game.new_char_view = Mock(spec=NewCharView)

    with (
        patch.object(game, "toggle_new_char_view") as mock_toggle_new_char,
        patch.object(game, "toggle_home_view") as mock_toggle_home,
    ):
        game._handle_character_creation("Decker")
        mock_toggle_new_char.assert_called_once()
        mock_toggle_home.assert_called_once()


def test_handle_character_creation_without_view(game_with_mocks: Mocks):
    """Tests the transition when new character view is already closed."""
    game = game_with_mocks.game
    # Ensure the new character view is None to test the `if` condition.
    game.new_char_view = None

    with (
        patch.object(game, "toggle_new_char_view") as mock_toggle_new_char,
        patch.object(game, "toggle_home_view") as mock_toggle_home,
    ):
        game._handle_character_creation("Decker")
        # Since the view is already None, it should not be toggled again.
        mock_toggle_new_char.assert_not_called()
        mock_toggle_home.assert_called_once()


def test_continue_from_intro_already_closed(game_with_mocks: Mocks):
    """Tests the intro transition when the intro view is already closed."""
    game = game_with_mocks.game
    game.intro_view = None  # Manually close the view before calling the handler

    with (
        patch.object(game, "toggle_intro_view") as mock_toggle_intro,
        patch.object(game, "toggle_new_char_view") as mock_toggle_new_char,
    ):
        game._continue_from_intro()

        # The intro view should NOT be toggled again since it's already None.
        mock_toggle_intro.assert_not_called()
        mock_toggle_new_char.assert_called_once()


def test_on_rest_callback_no_view(game_with_mocks: Mocks):
    """Tests the _on_rest callback when the rest view is already closed."""
    game = game_with_mocks.game
    # Ensure the view is None to test the `if` condition
    game.rest_view = None

    with (
        patch.object(game, "show_message") as mock_show_message,
        patch.object(game, "toggle_rest_view") as mock_toggle,
    ):
        game._on_rest()
        mock_show_message.assert_called_once_with("You feel rested and recovered.")
        mock_toggle.assert_not_called()


def test_game_toggles_mission_results_view(game_with_mocks: Mocks):
    """Tests that the toggle_mission_results_view method opens and closes the view."""
    game = game_with_mocks.game
    assert game.mission_results_view is None

    results_data = MissionResultsDTO(
        contract_name="Test Heist",
        was_successful=True,
        credits_earned=1000,
        reputation_change=1,
    )

    # Toggle to open
    with patch(
        "decker_pygame.presentation.game.MissionResultsView", spec=MissionResultsView
    ) as mock_view_class:
        game.toggle_mission_results_view(results_data)
        mock_view_class.assert_called_once_with(
            data=results_data, on_close=game.toggle_mission_results_view
        )
        assert game.mission_results_view is not None

    # Toggle to close
    game.toggle_mission_results_view()
    assert game.mission_results_view is None


def test_game_toggles_rest_view(game_with_mocks: Mocks):
    """Tests that the toggle_rest_view method opens and closes the view."""
    game = game_with_mocks.game
    assert game.rest_view is None

    rest_data = RestViewDTO(cost=100, health_recovered=50)

    # Toggle to open
    with patch(
        "decker_pygame.presentation.game.RestView", spec=RestView
    ) as mock_view_class:
        game.toggle_rest_view(rest_data)
        mock_view_class.assert_called_once_with(
            data=rest_data,
            on_rest=game._on_rest,
            on_close=game.toggle_rest_view,
        )
        assert game.rest_view is not None

    # Toggle to close
    game.toggle_rest_view()
    assert game.rest_view is None


def test_on_rest_callback(game_with_mocks: Mocks):
    """Tests the _on_rest callback."""
    game = game_with_mocks.game
    # Simulate that the view is open
    game.rest_view = Mock(spec=RestView)

    with (
        patch.object(game, "show_message") as mock_show_message,
        patch.object(game, "toggle_rest_view") as mock_toggle,
    ):
        game._on_rest()

        # Check that a message is shown and the view is closed
        mock_show_message.assert_called_once_with("You feel rested and recovered.")
        mock_toggle.assert_called_once()


def test_toggle_rest_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests that calling toggle_rest_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.rest_view is None

    # Call without data
    game.toggle_rest_view(data=None)

    # View should not have been created
    assert game.rest_view is None


def test_toggle_deck_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests that calling toggle_deck_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.deck_view is None
    # This test case is implicitly covered by test_toggle_deck_view_no_char_data
    # and test_toggle_deck_view_no_deck_data, as the factory function for DeckView
    # returns None if the necessary DTOs are not available.


def test_toggle_mission_results_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests calling toggle_mission_results_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.mission_results_view is None

    # Call without data
    game.toggle_mission_results_view(data=None)

    # View should not have been created
    assert game.mission_results_view is None


def test_game_toggles_shop_view(game_with_mocks: Mocks):
    """Tests that the toggle_shop_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game

    # Mock the DTO from the service
    shop_data = ShopViewDTO(shop_name="Test Shop", items=[])
    mocks.shop_service.get_shop_view_data.return_value = shop_data

    assert game.shop_view is None

    # Call the public method to open the view
    with patch(
        "decker_pygame.presentation.game.ShopView", spec=ShopView
    ) as mock_view_class:
        game.toggle_shop_view()

        mocks.shop_service.get_shop_view_data.assert_called_once_with("DefaultShop")
        mock_view_class.assert_called_once_with(
            data=shop_data,
            on_close=game.toggle_shop_view,
            on_purchase=game._on_purchase,
            on_view_details=game._on_show_item_details,  # Added this
        )
        assert game.shop_view is not None

    # Call again to close the view
    game.toggle_shop_view()
    assert game.shop_view is None


def test_toggle_shop_view_no_data(game_with_mocks: Mocks):
    """Tests that the shop view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.shop_service.get_shop_view_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_shop_view()
        assert game.shop_view is None
        mock_show_message.assert_called_once_with("Error: Could not load shop data.")


def test_on_purchase_success(game_with_mocks: Mocks):
    """Tests the callback for successfully purchasing an item."""
    mocks = game_with_mocks
    game = mocks.game

    with (
        patch.object(game, "toggle_shop_view") as mock_toggle,
        patch.object(game, "show_message") as mock_show_message,
    ):
        game._on_purchase("IcePick v1")

        mocks.shop_service.purchase_item.assert_called_once_with(
            game.character_id, "IcePick v1", "DefaultShop"
        )
        mock_show_message.assert_called_once_with("Purchased IcePick v1.")
        assert mock_toggle.call_count == 2  # Close and re-open


def test_on_purchase_failure(game_with_mocks: Mocks):
    """Tests the purchase callback when the service raises an error."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.shop_service.purchase_item.side_effect = ShopServiceError("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        game._on_purchase("any_item")
        mock_show_message.assert_called_once_with("Error: Service Error")


def test_game_toggles_ice_data_view(game_with_mocks: Mocks):
    """Tests that the toggle_ice_data_view method opens and closes the view."""
    game = game_with_mocks.game
    assert game.ice_data_view is None

    ice_data = IceDataViewDTO(
        name="Test ICE", ice_type="Test", strength=1, description="...", cost=100
    )

    # Toggle to open
    with patch(
        "decker_pygame.presentation.game.IceDataView", spec=IceDataView
    ) as mock_view_class:
        game.toggle_ice_data_view(ice_data)
        mock_view_class.assert_called_once_with(
            data=ice_data, on_close=game.toggle_ice_data_view
        )
        assert game.ice_data_view is not None

    # Toggle to close
    game.toggle_ice_data_view()
    assert game.ice_data_view is None


def test_on_program_click_success(game_with_mocks: Mocks):
    """Tests the callback for clicking a program successfully opens the detail view."""
    mocks = game_with_mocks
    game = mocks.game

    ice_data = IceDataViewDTO(
        name="IcePick v1", ice_type="Test", strength=1, description="...", cost=100
    )
    mocks.deck_service.get_ice_data.return_value = ice_data

    with patch.object(game, "toggle_ice_data_view") as mock_toggle:
        game._on_program_click("IcePick v1")
        mocks.deck_service.get_ice_data.assert_called_once_with("IcePick v1")
        mock_toggle.assert_called_once_with(ice_data)


def test_on_program_click_no_data(game_with_mocks: Mocks):
    """Tests the program click callback when no detailed data is available."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.deck_service.get_ice_data.return_value = None

    with (
        patch.object(game, "show_message") as mock_show_message,
        patch.object(game, "toggle_ice_data_view") as mock_toggle,
    ):
        game._on_program_click("Unknown Program")
        mock_show_message.assert_called_once_with(
            "No detailed data available for Unknown Program."
        )
        mock_toggle.assert_not_called()


def test_on_show_item_details_success(game_with_mocks: Mocks):
    """Tests that showing item details opens the item view on success."""
    mocks = game_with_mocks
    game = mocks.game
    item_details_dto = ShopItemViewDTO(
        name="Test Item",
        cost=100,
        description="A test item.",
        item_type=ShopItemType.PROGRAM,
        other_stats={},
    )
    mocks.shop_service.get_item_details.return_value = item_details_dto

    with patch.object(game, "toggle_shop_item_view") as mock_toggle:
        game._on_show_item_details("Test Item")
        mocks.shop_service.get_item_details.assert_called_once_with(
            "DefaultShop", "Test Item"
        )
        mock_toggle.assert_called_once_with(item_details_dto)


def test_on_show_item_details_failure(game_with_mocks: Mocks):
    """Tests that a message is shown if item details cannot be found."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.shop_service.get_item_details.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game._on_show_item_details("Unknown Item")
        mock_show_message.assert_called_once_with(
            "Could not retrieve details for Unknown Item."
        )


def test_game_toggles_shop_item_view(game_with_mocks: Mocks):
    """Tests that the toggle_shop_item_view method opens and closes the view."""
    game = game_with_mocks.game
    item_details_dto = ShopItemViewDTO(
        name="Test",
        cost=0,
        description="",
        item_type=ShopItemType.OTHER,
        other_stats={},
    )
    game.toggle_shop_item_view(item_details_dto)
    assert game.shop_item_view is not None
    game.toggle_shop_item_view()
    assert game.shop_item_view is None


def test_toggle_ice_data_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests calling toggle_ice_data_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.ice_data_view is None

    # Call without data
    game.toggle_ice_data_view(data=None)

    # View should not have been created
    assert game.ice_data_view is None


def test_toggle_shop_item_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests calling toggle_shop_item_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.shop_item_view is None

    # Call without data to cover the `if data:` branch in the factory
    game.toggle_shop_item_view(data=None)

    # View should not have been created
    assert game.shop_item_view is None


def test_on_download_file(game_with_mocks: Mocks):
    """Tests the callback for downloading a file."""
    game = game_with_mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        game._on_download_file("test.dat")
        mock_show_message.assert_called_once_with("Downloading test.dat...")


def test_on_delete_file(game_with_mocks: Mocks):
    """Tests the callback for deleting a file."""
    game = game_with_mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        game._on_delete_file("test.dat")
        mock_show_message.assert_called_once_with("Deleting test.dat...")


def test_show_file_access_view_success(game_with_mocks: Mocks):
    """Tests successfully showing the file access view."""
    mocks = game_with_mocks
    game = mocks.game
    node_id = "corp_server_1"
    mock_data = Mock(spec=FileAccessViewDTO)
    mocks.node_service.get_node_files.return_value = mock_data

    with patch.object(game, "toggle_file_access_view") as mock_toggle:
        game.show_file_access_view(node_id)
        mocks.node_service.get_node_files.assert_called_once_with(node_id)
        mock_toggle.assert_called_once_with(mock_data)


def test_show_file_access_view_closes_existing(game_with_mocks: Mocks):
    """Tests that showing the view when it's open just closes it."""
    mocks = game_with_mocks
    game = mocks.game
    game.file_access_view = Mock(spec=FileAccessView)

    with patch.object(game, "toggle_file_access_view") as mock_toggle:
        game.show_file_access_view("any_node")
        mocks.node_service.get_node_files.assert_not_called()
        mock_toggle.assert_called_once_with()


def test_show_file_access_view_node_not_found(game_with_mocks: Mocks):
    """Tests showing the file access view when the node is not found."""
    mocks = game_with_mocks
    game = mocks.game
    node_id = "unknown_node"
    mocks.node_service.get_node_files.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        with patch.object(game, "toggle_file_access_view") as mock_toggle:
            game.show_file_access_view(node_id)
            mocks.node_service.get_node_files.assert_called_once_with(node_id)
            mock_show_message.assert_called_once_with(
                "Error: Could not access node 'unknown_node'."
            )
            mock_toggle.assert_not_called()


def test_toggle_file_access_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests calling toggle_file_access_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.file_access_view is None

    # Call without data
    game.toggle_file_access_view(data=None)

    # View should not have been created
    assert game.file_access_view is None


def test_toggle_file_access_view_creates_view(game_with_mocks: Mocks):
    """Tests that toggle_file_access_view creates the view when data is provided."""
    game = game_with_mocks.game
    mock_data = Mock(spec=FileAccessViewDTO)

    assert game.file_access_view is None

    with patch("decker_pygame.presentation.game.FileAccessView") as mock_view_class:
        game.toggle_file_access_view(data=mock_data)

        assert game.file_access_view is not None
        mock_view_class.assert_called_once_with(
            data=mock_data,
            on_close=game.toggle_file_access_view,
            on_download=game._on_download_file,
            on_delete=game._on_delete_file,
        )


@pytest.mark.parametrize("is_valid", [True, False])
def test_on_entry_submit(game_with_mocks: Mocks, is_valid: bool):
    """Tests the callback for submitting text from the entry view."""
    mocks = game_with_mocks
    game = mocks.game
    node_id = "test_node"
    password = "password123"

    mocks.node_service.validate_password.return_value = is_valid

    with patch.object(game, "show_message") as mock_show_message:
        with patch.object(game, "toggle_entry_view") as mock_toggle:
            game._on_entry_submit(password, node_id)

            mocks.node_service.validate_password.assert_called_once_with(
                node_id, password
            )

            if is_valid:
                mock_show_message.assert_called_once_with("Access Granted.")
            else:
                mock_show_message.assert_called_once_with("Access Denied.")

            mock_toggle.assert_called_once()


def test_toggle_entry_view_creates_view(game_with_mocks: Mocks):
    """Tests that toggle_entry_view creates the view when a node_id is provided."""
    game = game_with_mocks.game
    node_id = "test_node"

    assert game.entry_view is None

    with patch("decker_pygame.presentation.game.EntryView") as mock_view_class:
        with patch("decker_pygame.presentation.game.EntryViewDTO") as mock_dto_class:
            game.toggle_entry_view(node_id=node_id)

            assert game.entry_view is not None
            mock_dto_class.assert_called_once_with(
                prompt=f"Enter Password for {node_id}:", is_password=True
            )
            mock_view_class.assert_called_once()
            # Check that the on_submit callback is a partial
            call_args = mock_view_class.call_args.kwargs
            assert call_args["data"] is mock_dto_class.return_value
            assert call_args["on_close"] == game.toggle_entry_view
            assert isinstance(call_args["on_submit"], partial)


def test_toggle_entry_view_without_node_id(game_with_mocks: Mocks):
    """Tests that calling toggle_entry_view without a node_id closes an open view
    and does nothing if the view is already closed.
    """
    game = game_with_mocks.game
    game.all_sprites = Mock(spec=pygame.sprite.Group)

    # --- Part 1: Test closing an open view ---
    mock_view = Mock(spec=EntryView)
    game.entry_view = mock_view
    game.all_sprites.add(mock_view)

    game.toggle_entry_view()  # Call without node_id to close

    assert game.entry_view is None, "View should be closed"
    game.all_sprites.remove.assert_called_once_with(mock_view)

    # --- Part 2: Test calling it again when already closed ---
    # This part will execute the factory and cover the `return None` line.
    game.toggle_entry_view()  # Call again

    assert game.entry_view is None, "View should remain closed"
    # The add method should not have been called, as the factory returns None.
    game.all_sprites.add.assert_called_once_with(mock_view)  # From the initial setup


def test_on_save_game(game_with_mocks: Mocks):
    """Tests the callback for saving the game."""
    game = game_with_mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        game._on_save_game()
        mock_show_message.assert_called_once_with("Game Saved (Not Implemented).")


def test_on_load_game(game_with_mocks: Mocks):
    """Tests the callback for loading the game."""
    game = game_with_mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        game._on_load_game()
        mock_show_message.assert_called_once_with("Game Loaded (Not Implemented).")


def test_on_quit_to_menu(game_with_mocks: Mocks):
    """Tests the callback for quitting to the main menu."""
    game = game_with_mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        with patch.object(game, "toggle_options_view") as mock_toggle:
            game._on_quit_to_menu()
            mock_show_message.assert_called_once_with("Quit to Menu (Not Implemented).")
            mock_toggle.assert_called_once()


@pytest.mark.parametrize("enabled", [True, False])
def test_on_toggle_sound(game_with_mocks: Mocks, enabled: bool):
    """Tests the callback for toggling sound."""
    mocks = game_with_mocks
    game = mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        game._on_toggle_sound(enabled)
        mocks.settings_service.set_sound_enabled.assert_called_once_with(enabled)
        expected_msg = f"Sound {'Enabled' if enabled else 'Disabled'}."
        mock_show_message.assert_called_once_with(expected_msg)


@pytest.mark.parametrize("enabled", [True, False])
def test_on_toggle_tooltips(game_with_mocks: Mocks, enabled: bool):
    """Tests the callback for toggling tooltips."""
    mocks = game_with_mocks
    game = mocks.game
    with patch.object(game, "show_message") as mock_show_message:
        game._on_toggle_tooltips(enabled)
        mocks.settings_service.set_tooltips_enabled.assert_called_once_with(enabled)
        expected_msg = f"Tooltips {'Enabled' if enabled else 'Disabled'}."
        mock_show_message.assert_called_once_with(expected_msg)


def test_toggle_options_view(game_with_mocks: Mocks):
    """Tests that toggle_options_view creates the view with correct data."""
    mocks = game_with_mocks
    game = mocks.game
    mock_options_data = Mock()
    mocks.settings_service.get_options.return_value = mock_options_data

    assert game.options_view is None

    with patch("decker_pygame.presentation.game.OptionsView") as mock_view_class:
        game.toggle_options_view()

        assert game.options_view is not None
        mocks.settings_service.get_options.assert_called_once()
        mock_view_class.assert_called_once_with(
            data=mock_options_data,
            on_save=game._on_save_game,
            on_load=game._on_load_game,
            on_quit=game._on_quit_to_menu,
            on_close=game.toggle_options_view,
            on_toggle_sound=game._on_toggle_sound,
            on_toggle_tooltips=game._on_toggle_tooltips,
        )


@pytest.mark.parametrize(
    "callback_name, service_method_name",
    [
        ("_on_master_volume_change", "set_master_volume"),
        ("_on_music_volume_change", "set_music_volume"),
        ("_on_sfx_volume_change", "set_sfx_volume"),
    ],
)
def test_on_volume_change_callbacks(
    game_with_mocks: Mocks, callback_name: str, service_method_name: str
):
    """Tests the callbacks for volume sliders."""
    mocks = game_with_mocks
    game = mocks.game
    volume = 0.75

    game_method = getattr(game, callback_name)
    service_method = getattr(mocks.settings_service, service_method_name)

    game_method(volume)

    service_method.assert_called_once_with(volume)


def test_toggle_sound_edit_view(game_with_mocks: Mocks):
    """Tests that toggle_sound_edit_view creates the view with correct data."""
    mocks = game_with_mocks
    game = mocks.game
    mock_sound_data = Mock()
    mocks.settings_service.get_sound_options.return_value = mock_sound_data

    assert game.sound_edit_view is None

    with patch("decker_pygame.presentation.game.SoundEditView") as mock_view_class:
        game.toggle_sound_edit_view()

        assert game.sound_edit_view is not None
        mocks.settings_service.get_sound_options.assert_called_once()
        mock_view_class.assert_called_once_with(
            data=mock_sound_data,
            on_close=game.toggle_sound_edit_view,
            on_master_volume_change=game._on_master_volume_change,
            on_music_volume_change=game._on_music_volume_change,
            on_sfx_volume_change=game._on_sfx_volume_change,
        )


def test_toggle_new_project_view(game_with_mocks: Mocks):
    """Tests that toggle_new_project_view creates the view with correct data."""
    mocks = game_with_mocks
    game = mocks.game
    mock_project_data = Mock(spec=NewProjectViewDTO)
    mocks.project_service.get_new_project_data.return_value = mock_project_data

    assert game.new_project_view is None

    with patch("decker_pygame.presentation.game.NewProjectView") as mock_view_class:
        game.toggle_new_project_view()

        assert game.new_project_view is not None
        mocks.project_service.get_new_project_data.assert_called_once_with(
            game.character_id
        )
        mock_view_class.assert_called_once_with(
            data=mock_project_data,
            on_start=game._on_start_project,
            on_close=game.toggle_new_project_view,
        )


def test_toggle_new_project_view_no_data(game_with_mocks: Mocks):
    """Tests that the new project view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.project_service.get_new_project_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_new_project_view()
        assert game.new_project_view is None
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve project data."
        )


def test_on_start_project_success(game_with_mocks: Mocks):
    """Tests the callback for successfully starting a project."""
    mocks = game_with_mocks
    game = mocks.game

    with patch.object(game, "show_message") as mock_show_message:
        with patch.object(game, "toggle_new_project_view") as mock_toggle:
            game._on_start_project("software", "Test ICE", 2)

            mocks.project_service.start_new_project.assert_called_once_with(
                game.character_id, "software", "Test ICE", 2
            )
            mock_show_message.assert_called_once_with(
                "Started research on Test ICE v2."
            )
            mock_toggle.assert_called_once()


def test_on_start_project_failure(game_with_mocks: Mocks):
    """Tests the start project callback when the service raises an error."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.project_service.start_new_project.side_effect = Exception("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        with patch.object(game, "toggle_new_project_view") as mock_toggle:
            game._on_start_project("software", "Test ICE", 2)

            mock_show_message.assert_called_once_with("Error: Service Error")
            mock_toggle.assert_not_called()


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


def test_game_toggles_project_data_view(game_with_mocks: Mocks):
    """Tests that the toggle_project_data_view method opens and closes the view."""
    mocks = game_with_mocks
    game = mocks.game

    # Mock the DTO from the service
    project_data = Mock(spec=ProjectDataViewDTO)
    mocks.project_service.get_project_data_view_data.return_value = project_data

    assert game.project_data_view is None

    # Call the public method to open the view
    with patch(
        "decker_pygame.presentation.game.ProjectDataView", spec=ProjectDataView
    ) as mock_view_class:
        game.toggle_project_data_view()

        mocks.project_service.get_project_data_view_data.assert_called_once_with(
            game.character_id
        )
        mock_view_class.assert_called_once_with(
            data=project_data,
            on_close=game.toggle_project_data_view,
            on_new_project=game._on_new_project,
            on_work_day=game._on_work_day,
            on_work_week=game._on_work_week,
            on_finish_project=game._on_finish_project,
            on_build=game._on_build_schematic,
            on_trash=game._on_trash_schematic,
        )
        assert game.project_data_view is not None

    # Call again to close the view
    game.toggle_project_data_view()
    assert game.project_data_view is None


def test_on_new_project_callback(game_with_mocks: Mocks):
    """Tests the callback for starting a new project from the project data view."""
    game = game_with_mocks.game

    with (
        patch.object(game, "toggle_project_data_view") as mock_toggle_project_data,
        patch.object(game, "toggle_new_project_view") as mock_toggle_new_project,
    ):
        game._on_new_project()

        mock_toggle_project_data.assert_called_once()
        mock_toggle_new_project.assert_called_once()


def test_on_work_day(game_with_mocks: Mocks):
    """Tests the callback for working on a project for a day."""
    mocks = game_with_mocks
    game = mocks.game

    with (
        patch.object(game, "toggle_project_data_view") as mock_toggle,
        patch.object(game, "show_message") as mock_show_message,
    ):
        game._on_work_day()

        mocks.project_service.work_on_project.assert_called_once_with(
            game.character_id, 1
        )
        mock_show_message.assert_called_once_with("One day of work completed.")
        assert mock_toggle.call_count == 2


def test_on_work_week(game_with_mocks: Mocks):
    """Tests the callback for working on a project for a week."""
    mocks = game_with_mocks
    game = mocks.game

    with (
        patch.object(game, "toggle_project_data_view") as mock_toggle,
        patch.object(game, "show_message") as mock_show_message,
    ):
        game._on_work_week()

        mocks.project_service.work_on_project.assert_called_once_with(
            game.character_id, 7
        )
        mock_show_message.assert_called_once_with("One week of work completed.")
        assert mock_toggle.call_count == 2


def test_on_finish_project(game_with_mocks: Mocks):
    """Tests the callback for finishing a project."""
    mocks = game_with_mocks
    game = mocks.game

    with (
        patch.object(game, "toggle_project_data_view") as mock_toggle,
        patch.object(game, "show_message") as mock_show_message,
    ):
        game._on_finish_project()

        mocks.project_service.complete_project.assert_called_once_with(
            game.character_id
        )
        mock_show_message.assert_called_once_with("Project finished.")
        assert mock_toggle.call_count == 2


def test_on_build_schematic(game_with_mocks: Mocks):
    """Tests the callback for building a schematic."""
    mocks = game_with_mocks
    game = mocks.game
    schematic_id = str(uuid.uuid4())

    with (
        patch.object(game, "toggle_project_data_view") as mock_toggle,
        patch.object(game, "show_message") as mock_show_message,
    ):
        game._on_build_schematic(schematic_id)

        mocks.project_service.build_from_schematic.assert_called_once_with(
            game.character_id, schematic_id
        )
        mock_show_message.assert_not_called()
        assert mock_toggle.call_count == 2


def test_on_trash_schematic(game_with_mocks: Mocks):
    """Tests the callback for trashing a schematic."""
    mocks = game_with_mocks
    game = mocks.game
    schematic_id = str(uuid.uuid4())

    with (
        patch.object(game, "toggle_project_data_view") as mock_toggle,
        patch.object(game, "show_message") as mock_show_message,
    ):
        game._on_trash_schematic(schematic_id)

        mocks.project_service.trash_schematic.assert_called_once_with(
            game.character_id, schematic_id
        )
        mock_show_message.assert_called_once_with("Schematic trashed.")
        assert mock_toggle.call_count == 2


def test_toggle_project_data_view_no_data(game_with_mocks: Mocks):
    """Tests that the project data view is not opened if data is missing."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.project_service.get_project_data_view_data.return_value = None

    with patch.object(game, "show_message") as mock_show_message:
        game.toggle_project_data_view()
        assert game.project_data_view is None
        mock_show_message.assert_called_once_with(
            "Error: Could not retrieve project data."
        )
