from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import ShopItemDTO, ShopViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.shop_view import ShopView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_shop_view_initialization():
    """Tests that the ShopView initializes and renders its data."""
    mock_on_close = Mock()
    mock_on_purchase = Mock()
    view_data = ShopViewDTO(
        shop_name="Test Shop",
        items=[
            ShopItemDTO(name="IcePick", cost=500, description="A basic tool."),
            ShopItemDTO(name="Hammer", cost=1200, description="A heavy tool."),
        ],
    )

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.shop_view.Button"
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        mock_button_instance = Mock(spec=Button)
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.return_value = mock_button_instance

        view = ShopView(
            data=view_data,
            on_close=mock_on_close,
            on_purchase=mock_on_purchase,  # Added Mock for on_view_details
            on_view_details=Mock(),
        )

        assert view is not None
        # Title + 2 item names + 2 item descriptions
        assert mock_font_instance.render.call_count == 5
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = {call.args[0] for call in render_calls}
        assert "Test Shop" in rendered_texts
        assert "IcePick - $500" in rendered_texts
        assert "  A basic tool." in rendered_texts
        assert "Hammer - $1200" in rendered_texts
        assert "  A heavy tool." in rendered_texts

        # Close button + 2 buy buttons
        assert mock_button_class.call_count == 5


def test_shop_view_delegates_purchase_event():
    """Tests that clicking a buy button triggers the on_purchase callback."""
    mock_on_close = Mock()
    mock_on_purchase = Mock()
    view_data = ShopViewDTO(
        shop_name="Test Shop",
        items=[ShopItemDTO(name="IcePick", cost=500, description="A basic tool.")],
    )

    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface(
            (100, 20)
        )  # Added parenthesis

        # mock_font_instance.render.return_value = pygame.Surface((100, 20))

        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        # Use real buttons to test the click interaction
        view = ShopView(
            data=view_data,
            on_close=mock_on_close,
            on_purchase=mock_on_purchase,
            on_view_details=Mock(),
        )

        # Find the "Buy" button for "IcePick"
        buy_button = next(
            c
            for c in view._components.sprites()
            if isinstance(c, Button) and c.text == "Buy"
        )

        # The button's rect is relative to the view. The click event needs to be
        # in screen space.
        click_pos = (
            buy_button.rect.centerx + view.rect.x,
            buy_button.rect.centery + view.rect.y,
        )
        down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
        )
        up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos}
        )

        view.handle_event(down_event)
        view.handle_event(up_event)

        mock_on_purchase.assert_called_once_with("IcePick")
        mock_on_close.assert_not_called()


def test_shop_view_delegates_view_details_event():
    """Tests that clicking the "View" button triggers the on_view_details callback."""
    mock_on_close = Mock()
    mock_on_purchase = Mock()
    mock_on_view_details = Mock()
    view_data = ShopViewDTO(
        shop_name="Test Shop",
        items=[ShopItemDTO(name="IcePick", cost=500, description="A basic tool.")],
    )

    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        # Use real buttons to test the click interaction
        view = ShopView(
            data=view_data,
            on_close=mock_on_close,
            on_purchase=mock_on_purchase,
            on_view_details=mock_on_view_details,
        )

        # Find the "View" button for "IcePick"
        view_button = next(
            c
            for c in view._components.sprites()
            if isinstance(c, Button) and c.text == "View"
        )

        # Simulate a click on the "View" button
        click_pos = (
            view_button.rect.centerx + view.rect.x,
            view_button.rect.centery + view.rect.y,
        )
        down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
        )
        up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos}
        )
        view.handle_event(down_event)
        view.handle_event(up_event)

        mock_on_view_details.assert_called_once_with("IcePick")
