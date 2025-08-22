"""Tests for the ShopState class."""

from unittest.mock import Mock, patch

import pytest

from decker_pygame.application.dtos import ShopItemViewDTO, ShopViewDTO
from decker_pygame.application.shop_service import ShopServiceError
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.states.home_state import HomeState
from decker_pygame.presentation.states.shop_state import ShopState


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object with mock services and a ViewManager."""
    game = Mock(spec=Game)
    game.view_manager = Mock()
    game.shop_service = Mock()
    return game


@pytest.fixture
def shop_state(mock_game: Mock) -> ShopState:
    """Provides a ShopState instance with a mocked Game."""
    return ShopState(mock_game)


def test_enter_creates_and_shows_view(shop_state: ShopState, mock_game: Mock):
    """Tests that entering the state creates and shows the ShopView."""
    mock_game.shop_service.get_shop_view_data.return_value = ShopViewDTO(
        shop_name="Test Shop", items=[]
    )

    with patch(
        "decker_pygame.presentation.states.shop_state.ShopView"
    ) as mock_shop_view_class:
        shop_state.enter()

        mock_game.view_manager.toggle_view.assert_called_once()
        args, _ = mock_game.view_manager.toggle_view.call_args
        assert args[0] == "shop_view"
        factory = args[1]
        _ = factory()
        mock_shop_view_class.assert_called_once_with(
            data=mock_game.shop_service.get_shop_view_data.return_value,
            on_close=shop_state._on_close,
            on_purchase=shop_state._on_purchase,
            on_view_details=shop_state._on_show_item_details,
        )


def test_enter_handles_no_shop_data(shop_state: ShopState, mock_game: Mock):
    """Tests that the state transitions back if shop data cannot be loaded."""
    mock_game.shop_service.get_shop_view_data.return_value = None

    shop_state.enter()

    mock_game.show_message.assert_called_once_with("Error: Could not load shop data.")
    mock_game.set_state.assert_called_once()
    assert isinstance(mock_game.set_state.call_args.args[0], HomeState)


def test_exit_closes_views(shop_state: ShopState, mock_game: Mock):
    """Tests that exiting the state closes all managed views."""
    shop_state.exit()

    assert mock_game.view_manager.toggle_view.call_count == 2
    mock_game.view_manager.toggle_view.assert_any_call("shop_view", None, mock_game)
    mock_game.view_manager.toggle_view.assert_any_call(
        "shop_item_view", None, mock_game
    )


def test_on_close_transitions_to_home_state(shop_state: ShopState, mock_game: Mock):
    """Tests that the _on_close callback transitions to the HomeState."""
    shop_state._on_close()
    mock_game.set_state.assert_called_once()
    assert isinstance(mock_game.set_state.call_args.args[0], HomeState)


def test_on_purchase_refreshes_state(shop_state: ShopState, mock_game: Mock):
    """Tests that a successful purchase refreshes the state."""
    with (
        patch.object(shop_state, "exit") as mock_exit,
        patch.object(shop_state, "enter") as mock_enter,
    ):
        shop_state._on_purchase("Test Item")
        mock_game.shop_service.purchase_item.assert_called_once()
        mock_exit.assert_called_once()
        mock_enter.assert_called_once()


def test_on_purchase_handles_error(shop_state: ShopState, mock_game: Mock):
    """Tests that a failed purchase shows an error message."""
    mock_game.shop_service.purchase_item.side_effect = ShopServiceError("No money")
    shop_state._on_purchase("Test Item")
    mock_game.show_message.assert_called_once_with("Error: No money")


def test_on_show_item_details(shop_state: ShopState, mock_game: Mock):
    """Tests showing the item details view."""
    mock_dto = Mock(spec=ShopItemViewDTO)
    mock_game.shop_service.get_item_details.return_value = mock_dto
    with patch.object(shop_state, "_toggle_shop_item_view") as mock_toggle:
        shop_state._on_show_item_details("Test Item")
        mock_toggle.assert_called_once_with(mock_dto)
