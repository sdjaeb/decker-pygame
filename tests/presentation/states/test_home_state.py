"""Tests for the HomeState class."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.domain.ids import ContractId
from decker_pygame.domain.project import Schematic, WorkUnit
from decker_pygame.application.dtos import (
    CharDataViewDTO,
    ContractDataViewDTO,
    ContractListViewDTO,
    BuildViewDTO,
    DeckViewDTO,
    IceDataViewDTO,
    ProjectDataViewDTO,
    TransferViewDTO,
    OrderViewDTO,
)
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.states.shop_state import ShopState
from decker_pygame.presentation.states.home_state import HomeState


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object with a mock ViewManager."""
    game = Mock(spec=Game)
    game.view_manager = Mock()
    game.character_service = Mock()
    game.deck_service = Mock()
    game.contract_service = Mock()
    game.project_service = Mock()
    game.character_id = "test_char_id"
    return game


@pytest.fixture
def home_state(mock_game: Mock) -> HomeState:
    """Provides a HomeState instance with a mocked Game."""
    return HomeState(mock_game)


def test_enter_creates_and_shows_view(home_state: HomeState, mock_game: Mock):
    """Tests that entering the state creates and shows the HomeView."""
    with patch(
        "decker_pygame.presentation.states.home_state.HomeView"
    ) as mock_home_view_class:
        home_state.enter()

        # Assert that the view manager was called to toggle the view
        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args

        # Check the arguments passed to toggle_view
        assert args[0] == "home_view"
        factory = args[1]
        assert callable(factory)
        assert args[2] is mock_game

        # Check that the factory function creates the HomeView with correct callbacks
        _ = factory()
        mock_home_view_class.assert_called_once_with(
            on_char=home_state._on_char,
            on_deck=home_state._on_deck,
            on_contracts=home_state._on_contracts,
            on_build=home_state._on_build,
            on_shop=home_state._on_shop,
            on_transfer=home_state._on_transfer,
            on_projects=home_state._on_projects,
        )


def test_exit_closes_views(home_state: HomeState, mock_game: Mock):
    """Tests that exiting the state closes all managed views."""
    home_state.exit()

    assert mock_game.view_manager.toggle_view.call_count == 10
    mock_game.view_manager.toggle_view.assert_any_call("home_view", None, mock_game)
    mock_game.view_manager.toggle_view.assert_any_call(
        "char_data_view", None, mock_game
    )
    mock_game.view_manager.toggle_view.assert_any_call("deck_view", None, mock_game)
    mock_game.view_manager.toggle_view.assert_any_call("order_view", None, mock_game)
    mock_game.view_manager.toggle_view.assert_any_call(
        "ice_data_view", None, mock_game
    )
    mock_game.view_manager.toggle_view.assert_any_call(
        "contract_list_view", None, mock_game
    )
    mock_game.view_manager.toggle_view.assert_any_call(
        "contract_data_view", None, mock_game
    )
    mock_game.view_manager.toggle_view.assert_any_call(
        "build_view", None, mock_game
    )
    mock_game.view_manager.toggle_view.assert_any_call(
        "transfer_view", None, mock_game
    )
    mock_game.view_manager.toggle_view.assert_any_call(
        "project_data_view", None, mock_game
    )


def test_on_char_toggles_char_data_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_char toggles the CharDataView when data is available."""
    mock_char_data = Mock(spec=CharDataViewDTO)
    mock_game.character_service.get_char_data_view_data.return_value = mock_char_data

    with patch(
        "decker_pygame.presentation.states.home_state.CharDataView"
    ) as mock_char_data_view_class:
        home_state._on_char()

        mock_game.character_service.get_char_data_view_data.assert_called_once_with(
            mock_game.character_id
        )

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "char_data_view"
        factory = args[1]
        _ = factory()

        mock_char_data_view_class.assert_called_once_with(
            data=mock_char_data, on_close=home_state._on_char
        )


def test_on_char_handles_no_data(home_state: HomeState, mock_game: Mock):
    """Tests that _on_char shows a message if no character data is found."""
    mock_game.character_service.get_char_data_view_data.return_value = None

    home_state._on_char()

    mock_game.view_manager.toggle_view.assert_called_once()
    args, _ = mock_game.view_manager.toggle_view.call_args
    assert args[0] == "char_data_view"
    factory = args[1]
    result = factory()

    assert result is None
    mock_game.show_message.assert_called_once_with("Could not load character data.")


def test_on_deck_toggles_deck_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_deck toggles the DeckView when data is available."""
    mock_deck_data = Mock(spec=DeckViewDTO)
    mock_game.deck_service.get_deck_view_data.return_value = mock_deck_data

    with patch(
        "decker_pygame.presentation.states.home_state.DeckView"
    ) as mock_deck_view_class:
        home_state._on_deck()

        mock_game.deck_service.get_deck_view_data.assert_called_once_with(
            mock_game.character_id
        )

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "deck_view"
        factory = args[1]
        _ = factory()

        mock_deck_view_class.assert_called_once_with(
            data=mock_deck_data,
            on_close=home_state._on_deck,
            on_order=home_state._toggle_order_view,
            on_program_click=home_state._on_program_click,
        )


def test_on_deck_handles_no_data(home_state: HomeState, mock_game: Mock):
    """Tests that _on_deck shows a message if no deck data is found."""
    mock_game.deck_service.get_deck_view_data.return_value = None

    home_state._on_deck()

    mock_game.view_manager.toggle_view.assert_called_once()
    args, _ = mock_game.view_manager.toggle_view.call_args
    assert args[0] == "deck_view"
    factory = args[1]
    result = factory()

    assert result is None
    mock_game.show_message.assert_called_once_with("Could not load deck data.")


def test_toggle_order_view_toggles_view(home_state: HomeState, mock_game: Mock):
    """Tests that _toggle_order_view toggles the OrderView when data is available."""
    mock_order_data = Mock(spec=OrderViewDTO)
    mock_game.deck_service.get_order_view_data.return_value = mock_order_data

    with patch(
        "decker_pygame.presentation.states.home_state.OrderView"
    ) as mock_order_view_class:
        home_state._toggle_order_view()

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "order_view"
        factory = args[1]
        _ = factory()

        mock_order_view_class.assert_called_once_with(
            data=mock_order_data,
            on_close=home_state._toggle_order_view,
            on_save=home_state._on_order_deck,
        )


def test_on_order_deck_saves_and_refreshes(home_state: HomeState, mock_game: Mock):
    """Tests that _on_order_deck saves the new order and refreshes views."""
    new_order = ["prog1", "prog2"]
    with patch.object(home_state, "_toggle_order_view") as mock_toggle_order, patch.object(
        home_state, "_on_deck"
    ) as mock_on_deck:
        home_state._on_order_deck(new_order)

        mock_game.deck_service.reorder_deck.assert_called_once_with(
            mock_game.character_id, new_order
        )
        mock_toggle_order.assert_called_once()
        assert mock_on_deck.call_count == 2


def test_on_program_click_toggles_ice_data_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_program_click toggles the IceDataView when data is available."""
    mock_ice_data = Mock(spec=IceDataViewDTO)
    mock_game.deck_service.get_ice_data_view_data.return_value = mock_ice_data

    with patch.object(
        home_state, "_toggle_ice_data_view"
    ) as mock_toggle_ice_data_view:
        home_state._on_program_click("TestProgram")

        mock_game.deck_service.get_ice_data_view_data.assert_called_once_with(
            "TestProgram"
        )
        mock_toggle_ice_data_view.assert_called_once_with(mock_ice_data)


def test_on_program_click_handles_no_data(home_state: HomeState, mock_game: Mock):
    """Tests that _on_program_click shows a message if no ICE data is found."""
    mock_game.deck_service.get_ice_data_view_data.return_value = None

    home_state._on_program_click("TestProgram")

    mock_game.show_message.assert_called_once_with(
        "Could not get data for TestProgram"
    )


def test_on_contracts_toggles_contract_list_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_contracts toggles the ContractListView when data is available."""
    mock_contract_list_data = Mock(spec=ContractListViewDTO)
    mock_game.contract_service.get_contract_list_view_data.return_value = (
        mock_contract_list_data
    )

    with patch(
        "decker_pygame.presentation.states.home_state.ContractListView"
    ) as mock_view_class:
        home_state._on_contracts()

        mock_game.contract_service.get_contract_list_view_data.assert_called_once_with(
            mock_game.character_id
        )

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "contract_list_view"
        factory = args[1]
        _ = factory()

        mock_view_class.assert_called_once_with(
            data=mock_contract_list_data,
            on_close=home_state._on_contracts,
            on_view_contract=home_state._on_view_contract,
        )


def test_on_contracts_handles_no_data(home_state: HomeState, mock_game: Mock):
    """Tests that _on_contracts shows a message if no contract list data is found."""
    mock_game.contract_service.get_contract_list_view_data.return_value = None

    home_state._on_contracts()

    mock_game.view_manager.toggle_view.assert_called_once()
    args, _ = mock_game.view_manager.toggle_view.call_args
    assert args[0] == "contract_list_view"
    factory = args[1]
    result = factory()

    assert result is None
    mock_game.show_message.assert_called_once_with("Could not load contract list.")


def test_on_view_contract_toggles_contract_data_view(
    home_state: HomeState, mock_game: Mock
):
    """Tests that _on_view_contract toggles the ContractDataView when data is available."""
    mock_contract_data = Mock(spec=ContractDataViewDTO)
    contract_id = ContractId()
    mock_game.contract_service.get_contract_data_view_data.return_value = (
        mock_contract_data
    )

    with patch.object(
        home_state, "_toggle_contract_data_view"
    ) as mock_toggle_view:
        home_state._on_view_contract(contract_id)

        mock_game.contract_service.get_contract_data_view_data.assert_called_once_with(
            contract_id
        )
        mock_toggle_view.assert_called_once_with(mock_contract_data)


def test_on_view_contract_handles_no_data(home_state: HomeState, mock_game: Mock):
    """Tests that _on_view_contract shows a message if no contract data is found."""
    contract_id = ContractId()
    mock_game.contract_service.get_contract_data_view_data.return_value = None

    home_state._on_view_contract(contract_id)

    mock_game.show_message.assert_called_once_with(
        f"Could not get data for contract {contract_id}"
    )


def test_toggle_contract_data_view_closes_view(home_state: HomeState, mock_game: Mock):
    """Tests that _toggle_contract_data_view closes the view when called with no data."""
    home_state._toggle_contract_data_view(None)

    mock_game.view_manager.toggle_view.assert_called_once()
    args, _ = mock_game.view_manager.toggle_view.call_args
    assert args[0] == "contract_data_view"
    factory = args[1]
    result = factory()
    assert result is None


def test_on_build_toggles_build_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_build toggles the BuildView when data is available."""
    mock_build_data = Mock(spec=BuildViewDTO)
    mock_game.project_service.get_build_view_data.return_value = mock_build_data

    with patch(
        "decker_pygame.presentation.states.home_state.BuildView"
    ) as mock_view_class:
        home_state._on_build()

        mock_game.project_service.get_build_view_data.assert_called_once_with(
            mock_game.character_id
        )

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "build_view"
        factory = args[1]
        _ = factory()

        mock_view_class.assert_called_once_with(
            data=mock_build_data,
            on_close=home_state._on_build,
            on_build=home_state._on_build_program,
        )


def test_on_build_program_builds_and_refreshes(home_state: HomeState, mock_game: Mock):
    """Tests that _on_build_program builds the program and refreshes the view."""
    schematic = Mock(spec=Schematic)
    schematic.name = "TestProgram"
    with patch.object(home_state, "_on_build") as mock_on_build:
        home_state._on_build_program(schematic)

        mock_game.project_service.build_from_schematic.assert_called_once_with(
            mock_game.character_id, schematic
        )
        mock_game.show_message.assert_called_once_with(
            "Successfully built TestProgram."
        )
        assert mock_on_build.call_count == 2


def test_on_build_program_handles_error(home_state: HomeState, mock_game: Mock):
    """Tests that _on_build_program shows an error message on failure."""
    schematic = Mock(spec=Schematic)
    error = Exception("Build failed")
    mock_game.project_service.build_from_schematic.side_effect = error

    home_state._on_build_program(schematic)

    mock_game.show_message.assert_called_once_with(
        f"Error building program: {error}"
    )


def test_on_transfer_toggles_transfer_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_transfer toggles the TransferView when data is available."""
    mock_transfer_data = Mock(spec=TransferViewDTO)
    mock_game.character_service.get_transfer_view_data.return_value = (
        mock_transfer_data
    )

    with patch(
        "decker_pygame.presentation.states.home_state.TransferView"
    ) as mock_view_class:
        home_state._on_transfer()

        mock_game.character_service.get_transfer_view_data.assert_called_once_with(
            mock_game.character_id
        )

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "transfer_view"
        factory = args[1]
        _ = factory()

        mock_view_class.assert_called_once_with(
            data=mock_transfer_data,
            on_close=home_state._on_transfer,
            on_transfer=home_state._on_transfer_funds,
        )


def test_on_transfer_funds_transfers_and_refreshes(
    home_state: HomeState, mock_game: Mock
):
    """Tests that _on_transfer_funds transfers credits and refreshes the view."""
    with patch.object(home_state, "_on_transfer") as mock_on_transfer:
        home_state._on_transfer_funds("recipient", 100)

        mock_game.character_service.transfer_credits.assert_called_once_with(
            mock_game.character_id, "recipient", 100
        )
        mock_game.show_message.assert_called_once_with(
            "Successfully transferred 100 credits."
        )
        assert mock_on_transfer.call_count == 2


def test_on_transfer_funds_handles_error(home_state: HomeState, mock_game: Mock):
    """Tests that _on_transfer_funds shows an error message on failure."""
    error = Exception("Transfer failed")
    mock_game.character_service.transfer_credits.side_effect = error

    home_state._on_transfer_funds("recipient", 100)

    mock_game.show_message.assert_called_once_with(
        f"Error transferring funds: {error}"
    )


def test_on_projects_toggles_project_data_view(home_state: HomeState, mock_game: Mock):
    """Tests that _on_projects toggles the ProjectDataView when data is available."""
    mock_project_data = Mock(spec=ProjectDataViewDTO)
    mock_game.project_service.get_project_data_view_data.return_value = (
        mock_project_data
    )

    with patch(
        "decker_pygame.presentation.states.home_state.ProjectDataView"
    ) as mock_view_class:
        home_state._on_projects()

        mock_game.project_service.get_project_data_view_data.assert_called_once_with(
            mock_game.character_id
        )

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "project_data_view"
        factory = args[1]
        view_instance = factory()

        mock_view_class.assert_called_once_with(
            data=mock_project_data,
            on_close=home_state._on_projects,
            on_work=home_state._on_work_project,
            on_build=home_state._on_build_from_schematic,
            on_new=view_instance.on_new,
        )


def test_on_work_project_works_and_refreshes(home_state: HomeState, mock_game: Mock):
    """Tests that _on_work_project works on the project and refreshes the view."""
    with patch.object(home_state, "_on_projects") as mock_on_projects:
        home_state._on_work_project(WorkUnit.DAY)

        mock_game.project_service.work_on_project.assert_called_once_with(
            mock_game.character_id, WorkUnit.DAY
        )
        assert mock_on_projects.call_count == 2


def test_on_build_from_schematic_builds_and_refreshes(
    home_state: HomeState, mock_game: Mock
):
    """Tests that _on_build_from_schematic builds the program and refreshes."""
    schematic = Mock(spec=Schematic)
    schematic.name = "TestProgram"
    with patch.object(home_state, "_on_projects") as mock_on_projects:
        home_state._on_build_from_schematic(schematic)

        mock_game.project_service.build_from_schematic.assert_called_once_with(
            mock_game.character_id, schematic
        )
        mock_game.show_message.assert_called_once_with(
            "Successfully built TestProgram."
        )
        assert mock_on_projects.call_count == 2


def test_on_shop_transitions_to_shop_state(home_state: HomeState, mock_game: Mock):
    """Tests that the _on_shop callback transitions to the ShopState."""
    with patch("decker_pygame.presentation.states.home_state.ShopState") as MockShopState:
        # Call the method under test
        home_state._on_shop()

        # Assert that a new ShopState was created with the game instance
        MockShopState.assert_called_once_with(mock_game)

        # Assert that game.set_state was called with the new ShopState instance
        mock_game.set_state.assert_called_once_with(MockShopState.return_value)


def test_handle_event_delegates_to_view_manager(home_state: HomeState, mock_game: Mock):
    """Tests that handle_event is delegated to the view manager."""
    event = pygame.event.Event(pygame.KEYDOWN)
    home_state.handle_event(event)
    mock_game.view_manager.handle_event.assert_called_once_with(event)


def test_update_delegates_to_view_manager(home_state: HomeState, mock_game: Mock):
    """Tests that update is delegated to the view manager."""
    home_state.update(16, 1234)
    mock_game.view_manager.update.assert_called_once_with(16, 1234)


def test_get_sprites_returns_empty_list(home_state: HomeState):
    """Tests that get_sprites returns an empty list as the view manager handles sprites."""
    assert home_state.get_sprites() == []