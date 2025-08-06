"""Tests for the ShopItemView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import ShopItemViewDTO
from decker_pygame.domain.shop import ShopItemType
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.shop_item_view import ShopItemView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


OTHER_STATS_PLACEHOLDER = {"damage": 10, "capacity": 5}  # Example stats


def test_shop_item_view_initialization():
    """Tests that the ShopItemView initializes and renders its data."""
    mock_on_close = Mock()
    item_data = ShopItemViewDTO(
        name="Energy Cell",
        cost=100,
        description="A high-capacity energy cell.",
        item_type=ShopItemType.BATTERY,
        other_stats=OTHER_STATS_PLACEHOLDER,
    )

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.shop_item_view.Button"
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

        view = ShopItemView(data=item_data, on_close=mock_on_close)

        assert view is not None
        # Title + 4 details lines (Cost, Type, Description, damage, capacity)
        assert mock_font_instance.render.call_count == 6
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = {call.args[0] for call in render_calls}
        assert "Energy Cell" in rendered_texts
        assert "Cost: $100" in rendered_texts
        assert "Type: Battery" in rendered_texts  # Check enum value
        assert "Description: A high-capacity energy cell." in rendered_texts
        assert "damage: 10" in rendered_texts
        assert "capacity: 5" in rendered_texts

        # Close button
        mock_button_class.assert_called_once()


def test_shop_item_view_delegates_close_event():
    """Tests that clicking the close button triggers the on_close callback."""
    mock_on_close = Mock()
    item_data = ShopItemViewDTO(
        name="Energy Cell",
        cost=100,
        description="A high-capacity energy cell.",
        item_type=ShopItemType.BATTERY,
        other_stats=OTHER_STATS_PLACEHOLDER,
    )

    view = ShopItemView(data=item_data, on_close=mock_on_close)
    # The button click logic is already tested in Button, so we can call
    # handle_event with a dummy event.
    # Simulate a click on the close button
    click_pos = (
        view._close_button.rect.centerx + view.rect.x,
        view._close_button.rect.centery + view.rect.y,
    )
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
    )
    up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos})
    view.handle_event(down_event)
    view.handle_event(up_event)
    mock_on_close.assert_called_once()
