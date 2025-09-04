import uuid
from collections.abc import Generator
from dataclasses import dataclass
from functools import partial
from typing import cast
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import (
    FileAccessViewDTO,
    MissionResultsDTO,
    NewProjectViewDTO,
    ProjectDataViewDTO,
    RestViewDTO,
)
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    DeckServiceInterface,
    DSFileServiceInterface,
    LoggingServiceInterface,
    MatrixRunServiceInterface,
    NodeServiceInterface,
    PlayerServiceInterface,
    ProjectServiceInterface,
    SettingsServiceInterface,
    ShopServiceInterface,
)
from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.components.entry_view import EntryView
from decker_pygame.presentation.components.file_access_view import FileAccessView
from decker_pygame.presentation.components.matrix_run_view import (
    MatrixRunView,
)
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.components.mission_results_view import (
    MissionResultsView,
)
from decker_pygame.presentation.components.project_data_view import ProjectDataView
from decker_pygame.presentation.components.rest_view import RestView
from decker_pygame.presentation.debug_actions import DebugActions
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.input_handler import PygameInputHandler
from decker_pygame.presentation.states.game_states import BaseState, GameState
from decker_pygame.presentation.states.states import (
    IntroState,
)
from decker_pygame.presentation.view_manager import ViewManager
from decker_pygame.settings import FPS


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
    matrix_run_service: Mock
    logging_service: Mock
    event_dispatcher: Mock


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
    mock_matrix_run_service = Mock(spec=MatrixRunServiceInterface)
    mock_logging_service = Mock(spec=LoggingServiceInterface)
    mock_event_dispatcher = Mock(spec=EventDispatcher)
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
            matrix_run_service=mock_matrix_run_service,
            event_dispatcher=mock_event_dispatcher,
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
            matrix_run_service=mock_matrix_run_service,
            logging_service=mock_logging_service,
            event_dispatcher=mock_event_dispatcher,
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
    assert game.event_dispatcher is mocks.event_dispatcher
    assert isinstance(game.view_manager, ViewManager)
    assert isinstance(game.player_id, uuid.UUID)
    assert isinstance(game.debug_actions, DebugActions)
    assert isinstance(game.character_id, uuid.UUID)
    # State machine attributes
    assert len(game.states) == 4
    assert game.states[GameState.INTRO] is IntroState
    assert isinstance(game.current_state, IntroState)
    # The initial state should open the intro view
    assert game.intro_view is not None


def test_run_loop_calls_methods(game_with_mocks: Mocks):
    """Tests that the main loop calls its core methods."""
    game = game_with_mocks.game

    # Configure mock input handler to quit the game on the first call.
    game.input_handler.handle_events.side_effect = game.quit  # type: ignore[attr-defined]
    game.clock.tick.return_value = 16  # type: ignore[attr-defined]

    # Mock the current state to check for calls
    mock_state = Mock(spec=BaseState)
    game.current_state = mock_state

    game.run()

    game.input_handler.handle_events.assert_called_once()  # type: ignore[attr-defined]
    mock_state.update.assert_called_once_with(0.016)  # dt in seconds
    mock_state.draw.assert_called_once_with(game.screen)
    game.clock.tick.assert_called_once_with(FPS)  # type: ignore[attr-defined]


def test_game_quit_method(game_with_mocks: Mocks):
    """Tests that the public quit() method sets the is_running flag to False."""
    game = game_with_mocks.game
    assert game.is_running is True
    game.quit()
    assert game.is_running is False


def test_set_state_transitions_correctly(game_with_mocks: Mocks):
    """Tests that set_state calls on_exit and on_enter on the correct states."""
    game = game_with_mocks.game

    # Create mock state classes
    mock_state_a_instance = Mock(spec=BaseState)
    mock_state_a_class = Mock(return_value=mock_state_a_instance)

    mock_state_b_instance = Mock(spec=BaseState)
    mock_state_b_class = Mock(return_value=mock_state_b_instance)

    # Register the mock states
    game.states = {
        GameState.INTRO: cast(type[BaseState], mock_state_a_class),
        GameState.HOME: cast(type[BaseState], mock_state_b_class),
    }

    # --- Transition 1: from None to State A ---
    game.set_state(GameState.INTRO)

    # Assert State A was created and entered
    mock_state_a_class.assert_called_once_with(game)
    assert game.current_state is mock_state_a_instance
    mock_state_a_instance.on_enter.assert_called_once()
    mock_state_a_instance.on_exit.assert_not_called()

    # --- Transition 2: from State A to State B ---
    game.set_state(GameState.HOME)

    # Assert State A was exited
    mock_state_a_instance.on_exit.assert_called_once()

    # Assert State B was created and entered
    mock_state_b_class.assert_called_once_with(game)
    assert game.current_state is mock_state_b_instance
    mock_state_b_instance.on_enter.assert_called_once()


def test_set_state_to_quit(game_with_mocks: Mocks):
    """Tests that setting the state to QUIT calls the game's quit method."""
    game = game_with_mocks.game
    with patch.object(game, "quit") as mock_quit:
        game.set_state(GameState.QUIT)
        mock_quit.assert_called_once()


def test_set_state_to_unregistered_state_quits(game_with_mocks: Mocks):
    """Tests that setting the state to an unregistered enum quits the game."""
    game = game_with_mocks.game
    game.states = {}  # Ensure the state is not registered
    with patch.object(game, "quit") as mock_quit:
        game.set_state(GameState.MATRIX_RUN)
        mock_quit.assert_called_once()


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


def test_game_on_increase_skill_failure(game_with_mocks: Mocks):
    """Tests the callback for increasing a skill when the service fails."""
    mocks = game_with_mocks
    game = mocks.game
    mocks.character_service.increase_skill.side_effect = Exception("Service Error")

    with patch.object(game, "show_message") as mock_show_message:
        # This test is now more generic for the helper method
        game._execute_and_refresh_view(mocks.character_service.increase_skill, Mock())
        mock_show_message.assert_called_once_with("Error: Service Error")


def test_continue_from_intro_sets_state(game_with_mocks: Mocks):
    """Tests that _continue_from_intro transitions to the NEW_CHAR state."""
    game = game_with_mocks.game
    with patch.object(game, "set_state") as mock_set_state:
        game._continue_from_intro()
        mock_set_state.assert_called_once_with(GameState.NEW_CHAR)


def test_handle_character_creation_sets_state(game_with_mocks: Mocks):
    """Tests that _handle_character_creation transitions to the HOME state."""
    game = game_with_mocks.game
    with patch.object(game, "set_state") as mock_set_state:
        game._handle_character_creation("Decker")
        mock_set_state.assert_called_once_with(GameState.HOME)


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


def test_toggle_mission_results_view_without_data_does_nothing(game_with_mocks: Mocks):
    """Tests calling toggle_mission_results_view without data does not open the view."""
    game = game_with_mocks.game
    assert game.mission_results_view is None

    # Call without data
    game.toggle_mission_results_view(data=None)

    # View should not have been created
    assert game.mission_results_view is None


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

    with patch.object(
        game, "all_sprites", Mock(spec=pygame.sprite.Group)
    ) as mock_all_sprites:
        # --- Part 1: Test closing an open view ---
        mock_view = Mock(spec=EntryView)
        game.entry_view = mock_view
        mock_all_sprites.add(mock_view)

        game.toggle_entry_view()  # Call without node_id to close

        assert game.entry_view is None, "View should be closed"
        mock_all_sprites.remove.assert_called_once_with(mock_view)

        # --- Part 2: Test calling it again when already closed ---
        # This part will execute the factory and cover the `return None` line.
        game.toggle_entry_view()  # Call again

        assert game.entry_view is None, "View should remain closed"
        # The add method should not have been called again.
        mock_all_sprites.add.assert_called_once_with(mock_view)


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
