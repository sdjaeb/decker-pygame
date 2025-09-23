"""Tests for the concrete game state classes and their base protocol."""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.application.dtos import (
    CharacterViewDTO,
    ContractSummaryDTO,
    DeckViewDTO,
    IceDataViewDTO,
    ShopItemViewDTO,
    ShopViewDTO,
    TransferViewDTO,
)
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.char_data_view import CharDataView
from decker_pygame.presentation.components.contract_data_view import ContractDataView
from decker_pygame.presentation.components.contract_list_view import ContractListView
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.ice_data_view import IceDataView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.matrix_run_view import MatrixRunView
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.shop_item_view import ShopItemView
from decker_pygame.presentation.components.shop_view import ShopView
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.states.game_states import BaseState
from decker_pygame.presentation.states.states import (
    HomeState,
    IntroState,
    MatrixRunState,
    NewCharState,
)

if TYPE_CHECKING:
    from decker_pygame.presentation.game import Game


class DummyState(BaseState):
    """A concrete class for testing the BaseState protocol for coverage."""

    def __init__(self, game: "Game") -> None:
        """Initializes the dummy state."""

    def on_enter(self) -> None:
        """Dummy on_enter."""

    def on_exit(self) -> None:
        """Dummy on_exit."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Dummy handle_event."""

    def update(self, dt: float) -> None:
        """Dummy update."""

    def draw(self, screen: pygame.Surface) -> None:
        """Dummy draw."""


def test_base_state_protocol_coverage() -> None:
    """This test exists purely to satisfy coverage for the protocol definition."""
    mock_game = Mock()
    state = DummyState(mock_game)
    state.on_enter()
    state.on_exit()
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.1)
    state.draw(Mock(spec=pygame.Surface))


def test_intro_state_lifecycle() -> None:
    """Tests that IntroState correctly toggles the IntroView via the ViewManager."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = IntroState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "intro_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.IntroView", spec=IntroView
    ) as mock_intro_view_class:
        created_view = factory_arg()
        mock_intro_view_class.assert_called_once_with(
            on_continue=mock_game._continue_from_intro
        )
        assert created_view is mock_intro_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "intro_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)


def test_new_char_state_lifecycle() -> None:
    """Tests that NewCharState correctly toggles the NewCharView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = NewCharState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "new_char_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.NewCharView", spec=NewCharView
    ) as mock_view_class:
        created_view = factory_arg()
        mock_view_class.assert_called_once_with(
            on_create=mock_game._handle_character_creation
        )
        assert created_view is mock_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "new_char_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)


def test_home_state_lifecycle() -> None:
    """Tests that HomeState correctly toggles the HomeView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "home_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.HomeView", spec=HomeView
    ) as mock_view_class:
        created_view = factory_arg()
        mock_view_class.assert_called_once_with(
            on_char=state._toggle_char_data_view,
            on_deck=state._toggle_deck_view,
            on_contracts=state._toggle_contract_list_view,
            on_build=state._toggle_build_view,
            on_shop=state._toggle_shop_view,
            on_transfer=state._toggle_transfer_view,
            on_projects=mock_game.toggle_project_data_view,
        )
        assert created_view is mock_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "home_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)


def test_home_state_char_data_view_logic() -> None:
    """Tests the HomeState's logic for managing the CharDataView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test toggling the view ---
    # Mock the service call
    mock_view_data = Mock(spec=CharacterViewDTO)
    mock_game.character_service.get_character_view_data.return_value = mock_view_data

    with patch(
        "decker_pygame.presentation.states.states.CharDataView", spec=CharDataView
    ) as mock_char_view_class:
        state._toggle_char_data_view()
        mock_game.view_manager.toggle_view.assert_called_once()

        # Check factory
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_char_view_class.assert_called_once_with(
            position=(150, 100),
            data=mock_view_data,
            on_close=state._toggle_char_data_view,
            on_increase_skill=state._on_increase_skill,
            on_decrease_skill=state._on_decrease_skill,
        )
        assert created_view is mock_char_view_class.return_value

    # --- Test toggling with no data ---
    mock_game.reset_mock()
    mock_game.character_service.get_character_view_data.return_value = None
    state._toggle_char_data_view()
    # The factory will return None, so toggle_view is still called, but with a factory
    # that returns None.
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_once_with(
        "Error: Could not retrieve character/player data."
    )

    # --- Test skill increase callback ---
    mock_game.reset_mock()

    # Mock the executor to actually call the action it receives.
    def mock_executor(action, toggler):
        action()
        toggler()
        toggler()

    mock_game._execute_and_refresh_view.side_effect = mock_executor
    state._on_increase_skill("hacking")
    mock_game.character_service.increase_skill.assert_called_once_with(
        mock_game.character_id, "hacking"
    )
    mock_game._execute_and_refresh_view.assert_called_once()
    # Check that the correct view toggler was passed
    assert (
        mock_game._execute_and_refresh_view.call_args.args[1]
        == state._toggle_char_data_view
    )

    # --- Test skill decrease callback ---
    mock_game.reset_mock()
    mock_game._execute_and_refresh_view.side_effect = mock_executor
    state._on_decrease_skill("crafting")
    mock_game.character_service.decrease_skill.assert_called_once_with(
        mock_game.character_id, "crafting"
    )
    mock_game._execute_and_refresh_view.assert_called_once()
    assert (
        mock_game._execute_and_refresh_view.call_args.args[1]
        == state._toggle_char_data_view
    )


def test_home_state_deck_and_order_view_logic() -> None:
    """Tests the HomeState's logic for managing the DeckView and OrderView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # Mock service calls
    mock_char_data = Mock()
    mock_deck_data = Mock(spec=DeckViewDTO)
    mock_game.character_service.get_character_data.return_value = mock_char_data
    mock_game.deck_service.get_deck_view_data.return_value = mock_deck_data

    # --- Test _toggle_deck_view ---
    with patch(
        "decker_pygame.presentation.states.states.DeckView", spec=DeckView
    ) as mock_deck_view_class:
        state._toggle_deck_view()
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()
        mock_deck_view_class.assert_called_once_with(
            data=mock_deck_data,
            on_close=state._toggle_deck_view,
            on_order=state._handle_order_click,
            on_program_click=state._on_program_click,
        )
        assert created_view is mock_deck_view_class.return_value

    # --- Test _toggle_order_view ---
    mock_game.view_manager.reset_mock()
    with patch(
        "decker_pygame.presentation.states.states.OrderView", spec=OrderView
    ) as mock_order_view_class:
        state._toggle_order_view()
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()
        mock_order_view_class.assert_called_once_with(
            data=mock_deck_data,
            on_close=state._handle_order_close,
            on_move_up=state._on_move_program_up,
            on_move_down=state._on_move_program_down,
        )
        assert created_view is mock_order_view_class.return_value

    # --- Test transitions ---
    mock_game.view_manager.reset_mock()
    with patch.object(state, "_toggle_deck_view") as mock_toggle_deck:
        with patch.object(state, "_toggle_order_view") as mock_toggle_order:
            state._handle_order_click()
            mock_toggle_deck.assert_called_once()
            mock_toggle_order.assert_called_once()

            mock_toggle_deck.reset_mock()
            mock_toggle_order.reset_mock()

            state._handle_order_close()
            mock_toggle_deck.assert_called_once()
            mock_toggle_order.assert_called_once()

    # --- Test program move callbacks ---
    def mock_executor(action, toggler):
        action()

    mock_game.reset_mock()
    mock_game._execute_and_refresh_view.side_effect = mock_executor

    state._on_move_program_up("IcePick")
    mock_game.deck_service.move_program_up.assert_called_once_with(
        mock_char_data.deck_id, "IcePick"
    )
    assert (
        mock_game._execute_and_refresh_view.call_args.args[1]
        == state._toggle_order_view
    )

    mock_game.reset_mock()
    mock_game._execute_and_refresh_view.side_effect = mock_executor
    state._on_move_program_down("Hammer")
    mock_game.deck_service.move_program_down.assert_called_once_with(
        mock_char_data.deck_id, "Hammer"
    )

    # --- Test program click callback ---
    mock_game.reset_mock()
    mock_ice_data = Mock(spec=IceDataViewDTO)
    mock_game.deck_service.get_ice_data.return_value = mock_ice_data
    # Patch the state's own method to check the call
    with patch.object(state, "_toggle_ice_data_view") as mock_toggle_ice:
        state._on_program_click("IcePick")
        mock_toggle_ice.assert_called_once_with(mock_ice_data)

    # Test failure case
    mock_game.reset_mock()
    mock_game.deck_service.get_ice_data.return_value = None
    with patch.object(state, "_toggle_ice_data_view") as mock_toggle_ice:
        state._on_program_click("Unknown")
        mock_game.show_message.assert_called_once_with(
            "No detailed data available for Unknown."
        )
        mock_toggle_ice.assert_not_called()


def test_home_state_deck_and_order_view_failures() -> None:
    """Tests the failure paths for the DeckView and OrderView logic."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test failure when character data is missing ---
    mock_game.character_service.get_character_data.return_value = None

    # Test DeckView creation failure
    state._toggle_deck_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_with(
        "Error: Could not retrieve character data to find deck."
    )

    # Test OrderView creation failure
    state._toggle_order_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None

    # --- Test failure when deck data is missing ---
    mock_game.reset_mock()
    mock_game.character_service.get_character_data.return_value = Mock()
    mock_game.deck_service.get_deck_view_data.return_value = None
    state._toggle_deck_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_with("Error: Could not retrieve deck data.")


def test_home_state_perform_move_up_action_failure() -> None:
    """Tests the failure path for the move up action when character is not found."""
    mock_game = Mock()
    state = HomeState(mock_game)
    mock_game.character_service.get_character_data.return_value = None

    def mock_executor(action, toggler):
        try:
            action()
        except Exception as e:
            mock_game.show_message(f"Error: {e}")

    mock_game._execute_and_refresh_view.side_effect = mock_executor
    with pytest.raises(Exception, match="Could not find character to modify deck."):
        state._perform_move_up("any")


def test_home_state_toggle_order_view_no_deck_data() -> None:
    """Tests that the order view is not opened if deck data is missing."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # Simulate character data being found, but deck data is missing
    mock_game.character_service.get_character_data.return_value = Mock()
    mock_game.deck_service.get_deck_view_data.return_value = None

    state._toggle_order_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_once_with(
        "Error: Could not retrieve deck data."
    )


def test_home_state_perform_move_down_action_failure() -> None:
    """Tests the failure path for the move down action when character is not found."""
    mock_game = Mock()
    state = HomeState(mock_game)
    mock_game.character_service.get_character_data.return_value = None

    with pytest.raises(Exception, match="Could not find character to modify deck."):
        state._perform_move_down("any")


def test_home_state_on_show_item_details_failure() -> None:
    """Tests the failure path for showing item details."""
    mock_game = Mock()
    state = HomeState(mock_game)

    # --- Test _on_show_item_details failure ---
    mock_game.reset_mock()
    mock_game.shop_service.get_item_details.return_value = None
    with patch.object(state, "_toggle_shop_item_view") as mock_toggle_item:
        state._on_show_item_details("UnknownItem")
        mock_game.show_message.assert_called_once_with(
            "Could not retrieve details for UnknownItem."
        )
        mock_toggle_item.assert_not_called()


def test_home_state_contract_view_logic() -> None:
    """Tests the HomeState's logic for managing contract views."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test _toggle_contract_list_view success ---
    mock_contracts = [Mock(spec=ContractSummaryDTO)]
    mock_game.contract_service.get_available_contracts.return_value = mock_contracts
    with patch(
        "decker_pygame.presentation.states.states.ContractListView",
        spec=ContractListView,
    ) as mock_view_class:
        mock_view_instance = mock_view_class.return_value
        state._toggle_contract_list_view()

        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_view_class.assert_called_once_with(
            position=(200, 150),
            size=(450, 300),
            on_contract_selected=state._on_contract_selected,
        )
        mock_view_instance.set_contracts.assert_called_once_with(mock_contracts)
        assert created_view is mock_view_instance

    # --- Test _toggle_contract_list_view no contracts ---
    mock_game.reset_mock()
    mock_game.contract_service.get_available_contracts.return_value = []
    state._toggle_contract_list_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_once_with("No contracts available.")

    # --- Test _on_contract_selected with data ---
    mock_game.reset_mock()
    mock_dto = Mock(spec=ContractSummaryDTO)
    mock_dto.title = "Test Heist"
    mock_dto.id = "test_contract_id"
    with patch(
        "decker_pygame.presentation.states.states.ContractDataView",
        spec=ContractDataView,
    ) as mock_data_view_class:
        state._on_contract_selected(mock_dto)
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()
        mock_data_view_class.assert_called_once_with(
            position=(200, 150),
            size=(400, 300),
            contract=mock_dto,
            on_accept=state._on_accept_contract,
        )
        assert created_view is mock_data_view_class.return_value

    # --- Test _on_contract_selected with None ---
    mock_game.reset_mock()
    state._on_contract_selected(None)
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None

    # --- Test _on_accept_contract success ---
    mock_game.reset_mock()
    state._on_accept_contract(mock_dto.id)
    mock_game.contract_service.accept_contract.assert_called_once_with(
        mock_game.character_id, mock_dto.id
    )
    mock_game.set_state.assert_called_once()

    # --- Test _on_accept_contract failure ---
    mock_game.reset_mock()
    mock_game.contract_service.accept_contract.side_effect = Exception("Test Error")
    state._on_accept_contract(mock_dto.id)
    mock_game.show_message.assert_called_once_with(
        "Error accepting contract: Test Error"
    )
    mock_game.set_state.assert_not_called()


def test_home_state_ice_data_view_logic() -> None:
    """Tests the HomeState's logic for managing the IceDataView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test toggling the view with data ---
    mock_ice_data = Mock(spec=IceDataViewDTO)
    with patch(
        "decker_pygame.presentation.states.states.IceDataView", spec=IceDataView
    ) as mock_view_class:
        state._toggle_ice_data_view(mock_ice_data)
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_view_class.assert_called_once_with(
            data=mock_ice_data, on_close=state._toggle_ice_data_view
        )
        assert created_view is mock_view_class.return_value

    # --- Test toggling the view without data (to close it) ---
    mock_game.view_manager.reset_mock()
    state._toggle_ice_data_view(None)
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None


def test_home_state_build_view_logic() -> None:
    """Tests the HomeState's logic for managing the BuildView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test _toggle_build_view success ---
    mock_schematics = [Mock()]
    mock_game.crafting_service.get_character_schematics.return_value = mock_schematics
    with patch(
        "decker_pygame.presentation.states.states.BuildView", spec=BuildView
    ) as mock_view_class:
        state._toggle_build_view()
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_view_class.assert_called_once_with(
            position=(200, 150),
            size=(400, 300),
            schematics=mock_schematics,
            on_build_click=state._handle_build_click,
        )
        assert created_view is mock_view_class.return_value

    # --- Test _toggle_build_view no schematics ---
    mock_game.reset_mock()
    mock_game.crafting_service.get_character_schematics.return_value = []
    state._toggle_build_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_once_with("No schematics known.")

    # --- Test _handle_build_click success ---
    mock_game.reset_mock()
    state._handle_build_click("TestSchematic")
    mock_game.crafting_service.craft_item.assert_called_once_with(
        mock_game.character_id, "TestSchematic"
    )
    mock_game.show_message.assert_not_called()

    # --- Test _handle_build_click failure ---
    mock_game.reset_mock()
    mock_game.crafting_service.craft_item.side_effect = CraftingError("Test Error")
    state._handle_build_click("TestSchematic")
    mock_game.show_message.assert_called_once_with("Crafting failed: Test Error")


def test_home_state_shop_view_logic() -> None:
    """Tests the HomeState's logic for managing the ShopView and ShopItemView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test _toggle_shop_view success ---
    mock_shop_data = Mock(spec=ShopViewDTO)
    mock_game.shop_service.get_shop_view_data.return_value = mock_shop_data
    with patch(
        "decker_pygame.presentation.states.states.ShopView", spec=ShopView
    ) as mock_view_class:
        state._toggle_shop_view()
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_view_class.assert_called_once_with(
            data=mock_shop_data,
            on_close=state._toggle_shop_view,
            on_purchase=state._on_purchase,
            on_view_details=state._on_show_item_details,
        )
        assert created_view is mock_view_class.return_value

    # --- Test _toggle_shop_view no data ---
    mock_game.reset_mock()
    mock_game.shop_service.get_shop_view_data.return_value = None
    state._toggle_shop_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_once_with("Error: Could not load shop data.")

    # --- Test _on_purchase callback ---
    mock_game.reset_mock()

    def mock_executor(action, toggler):
        action()

    mock_game._execute_and_refresh_view.side_effect = mock_executor
    state._on_purchase("TestItem")
    mock_game.shop_service.purchase_item.assert_called_once_with(
        mock_game.character_id, "TestItem", "DefaultShop"
    )
    mock_game._execute_and_refresh_view.assert_called_once()
    assert (
        mock_game._execute_and_refresh_view.call_args.args[1] == state._toggle_shop_view
    )

    # --- Test _on_show_item_details success ---
    mock_game.reset_mock()
    mock_item_data = Mock(spec=ShopItemViewDTO)
    mock_game.shop_service.get_item_details.return_value = mock_item_data
    with patch.object(state, "_toggle_shop_item_view") as mock_toggle_item:
        state._on_show_item_details("TestItem")
        mock_toggle_item.assert_called_once_with(mock_item_data)

    # --- Test _on_show_item_details failure ---
    mock_game.reset_mock()
    mock_game.shop_service.get_item_details.return_value = None
    state._on_show_item_details("UnknownItem")
    mock_game.show_message.assert_called_once_with(
        "Could not retrieve details for UnknownItem."
    )

    # --- Test _perform_purchase (which is now trivial) ---
    mock_game.reset_mock()
    state._perform_purchase("TestItem")
    mock_game.shop_service.purchase_item.assert_called_once_with(
        mock_game.character_id, "TestItem", "DefaultShop"
    )
    mock_game.show_message.assert_called_once_with("Purchased TestItem.")

    # --- Test _toggle_shop_item_view factory ---
    mock_game.reset_mock()
    with patch(
        "decker_pygame.presentation.states.states.ShopItemView", spec=ShopItemView
    ) as mock_item_view_class:
        state._toggle_shop_item_view(mock_item_data)
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_item_view_class.assert_called_once_with(
            data=mock_item_data,
            on_close=state._toggle_shop_item_view,
        )
        assert created_view is mock_item_view_class.return_value

    # --- Test _toggle_shop_item_view with no data (to close) ---
    mock_game.reset_mock()
    state._toggle_shop_item_view(None)
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None


def test_home_state_transfer_view_logic() -> None:
    """Tests the HomeState's logic for managing the TransferView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test _toggle_transfer_view success ---
    mock_transfer_data = Mock(spec=TransferViewDTO)
    mock_game.deck_service.get_transfer_view_data.return_value = mock_transfer_data
    with patch(
        "decker_pygame.presentation.states.states.TransferView", spec=TransferView
    ) as mock_view_class:
        state._toggle_transfer_view()
        factory = mock_game.view_manager.toggle_view.call_args.args[1]
        created_view = factory()

        mock_view_class.assert_called_once_with(
            data=mock_transfer_data,
            on_close=state._toggle_transfer_view,
            on_move_to_deck=state._on_move_program_to_deck,
            on_move_to_storage=state._on_move_program_to_storage,
        )
        assert created_view is mock_view_class.return_value

    # --- Test _toggle_transfer_view no data ---
    mock_game.reset_mock()
    mock_game.deck_service.get_transfer_view_data.return_value = None
    state._toggle_transfer_view()
    factory = mock_game.view_manager.toggle_view.call_args.args[1]
    assert factory() is None
    mock_game.show_message.assert_called_once_with(
        "Error: Could not retrieve transfer data."
    )

    # --- Test _on_move_program_to_deck callback ---
    mock_game.reset_mock()

    def mock_executor(action, toggler):
        action()

    mock_game._execute_and_refresh_view.side_effect = mock_executor
    state._on_move_program_to_deck("TestProgram")
    mock_game.deck_service.move_program_to_deck.assert_called_once_with(
        mock_game.character_id, "TestProgram"
    )
    mock_game._execute_and_refresh_view.assert_called_once()
    assert (
        mock_game._execute_and_refresh_view.call_args.args[1]
        == state._toggle_transfer_view
    )

    # --- Test _on_move_program_to_storage callback ---
    mock_game.reset_mock()
    mock_game._execute_and_refresh_view.side_effect = mock_executor
    state._on_move_program_to_storage("TestProgram2")
    mock_game.deck_service.move_program_to_storage.assert_called_once_with(
        mock_game.character_id, "TestProgram2"
    )
    assert (
        mock_game._execute_and_refresh_view.call_args.args[1]
        == state._toggle_transfer_view
    )


def test_matrix_run_state_lifecycle() -> None:
    """Tests that MatrixRunState correctly toggles the MatrixRunView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = MatrixRunState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "matrix_run_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.MatrixRunView", spec=MatrixRunView
    ) as mock_view_class:
        created_view = factory_arg()
        mock_view_class.assert_called_once_with(asset_service=mock_game.asset_service)
        assert created_view is mock_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "matrix_run_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)
