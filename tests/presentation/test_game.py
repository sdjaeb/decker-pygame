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
from decker_pygame.application.deck_service import (
    DeckServiceError,
    DeckViewData,
    TransferViewData,
)
from decker_pygame.application.dtos import MissionResultsDTO, RestViewData
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
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.health_bar import HealthBar
from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.components.mission_results_view import (
    MissionResultsView,
)
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.rest_view import RestView
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.input_handler import PygameInputHandler
from decker_pygame.settings import FPS, GFX


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
    """Provides a fully mocked Game instance and its mocked dependencies."""
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
        patch(
            "decker_pygame.presentation.game.PygameInputHandler",
            spec=PygameInputHandler,
        ),
        patch(
            "decker_pygame.presentation.game.load_spritesheet",
            return_value=([pygame.Surface((16, 16))], (16, 16)),
        ),
        patch("decker_pygame.presentation.game.scale_icons") as mock_scale_icons,
    ):
        mock_scale_icons.return_value = [pygame.Surface((32, 32))]
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
            data=deck_data,
            on_close=game.toggle_deck_view,
            on_order=game._on_order_deck,
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
    transfer_data = TransferViewData(deck_programs=[], stored_programs=[])
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
        assert mock_toggle.call_count == 2


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
def test_on_move_program_failure(
    game_with_mocks: Mocks, method_to_test: str, service_method_to_mock: str
):
    """Tests the transfer callbacks when the service raises an error."""
    mocks = game_with_mocks
    game = mocks.game
    mock_service_method = getattr(mocks.deck_service, service_method_to_mock)
    mock_service_method.side_effect = DeckServiceError("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        game_method = getattr(game, method_to_test)
        game_method("AnyProgram")
        mock_show_message.assert_called_once_with("Error: Service Error")


def test_on_order_deck_success(game_with_mocks: Mocks):
    """Tests the successful path for the _on_order_deck callback."""
    mocks = game_with_mocks
    game = mocks.game

    # Set up a mock deck_view to be removed
    game.deck_view = Mock(spec=DeckView)
    game.all_sprites.add(game.deck_view)
    assert len(game.all_sprites) == 6

    # Configure services to return valid data
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    deck_data = DeckViewData(programs=[])
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
        assert len(game.all_sprites) == 6  # 5 base + 1 new OrderView


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
    game.all_sprites.add(existing_order_view)
    assert len(game.all_sprites) == 6

    # Configure services to return valid data
    mock_deck_id = DeckId(uuid.uuid4())
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    deck_data = DeckViewData(programs=[])
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
        assert len(game.all_sprites) == 6


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


@pytest.mark.parametrize(
    "method_to_test, service_method_to_mock",
    [
        ("_on_move_program_up", "move_program_up"),
        ("_on_move_program_down", "move_program_down"),
    ],
)
def test_on_move_program_order_failure(
    game_with_mocks: Mocks, method_to_test: str, service_method_to_mock: str
):
    """Tests the re-order callbacks when the service raises an error."""
    mocks = game_with_mocks
    game = mocks.game
    mock_deck_id = DeckId(uuid.uuid4())
    game_method = getattr(game, method_to_test)

    # Test service error case
    mocks.character_service.get_character_data.return_value = CharacterDataDTO(
        name="Testy", credits=0, skills={}, unused_skill_points=0, deck_id=mock_deck_id
    )
    mock_service_method = getattr(mocks.deck_service, service_method_to_mock)
    mock_service_method.side_effect = DeckServiceError("Service Error")
    with patch.object(game, "show_message") as mock_show_message:
        game_method("AnyProgram")
        mock_show_message.assert_called_once_with("Error: Service Error")

    # Test character not found case
    mocks.character_service.get_character_data.return_value = None
    with patch.object(game, "show_message") as mock_show_message:
        game_method("AnyProgram")
        mock_show_message.assert_called_once_with(
            "Error: Could not find character to modify deck."
        )


def test_game_toggles_home_view(game_with_mocks: Mocks):
    """Tests that the toggle_home_view method opens and closes the view."""
    game = game_with_mocks.game
    assert game.home_view is None

    # Toggle to open
    with patch(
        "decker_pygame.presentation.game.HomeView", spec=HomeView
    ) as mock_view_class:
        game.toggle_home_view()
        mock_view_class.assert_called_once()
        assert game.home_view is not None

    # Toggle to close
    game.toggle_home_view()
    assert game.home_view is None


def test_game_toggles_intro_view(game_with_mocks: Mocks):
    """Tests that the toggle_intro_view method opens and closes the view."""
    game = game_with_mocks.game
    # It starts open from __init__, so it should exist
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

    rest_data = RestViewData(cost=100, health_recovered=50)

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


def test_toggle_mission_results_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests calling toggle_mission_results_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.mission_results_view is None

    # Call without data
    game.toggle_mission_results_view(data=None)

    # View should not have been created
    assert game.mission_results_view is None
