from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import DeckViewDTO, ProgramDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.order_view import OrderView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_order_view_initialization():
    """Tests that the OrderView initializes and renders its data."""
    mock_on_close = Mock()
    mock_on_move_up = Mock()
    mock_on_move_down = Mock()
    view_data = DeckViewDTO(
        programs=[
            ProgramDTO(name="IcePick", size=10),
            ProgramDTO(name="Hammer", size=20),
        ],
        used_deck_size=30,
        total_deck_size=100,
    )

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.order_view.Button"
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

        view = OrderView(
            data=view_data,
            on_close=mock_on_close,
            on_move_up=mock_on_move_up,
            on_move_down=mock_on_move_down,
        )

        assert view is not None
        # 2 programs
        assert mock_font_instance.render.call_count == 2
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]
        assert "1. IcePick" in rendered_texts
        assert "2. Hammer" in rendered_texts

        # 1 close button + 1 "Up" button (for Hammer) + 1 "Down" button (for IcePick)
        assert mock_button_class.call_count == 3


def test_order_view_button_clicks():
    """Tests that clicking the up/down buttons triggers the correct callbacks."""
    mock_on_close = Mock()
    mock_on_move_up = Mock()
    mock_on_move_down = Mock()
    view_data = DeckViewDTO(
        programs=[
            ProgramDTO(name="IcePick", size=10),
            ProgramDTO(name="Hammer", size=20),
        ],
        used_deck_size=30,
        total_deck_size=100,
    )

    # We use real buttons for this test to verify the whole interaction
    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        view = OrderView(
            data=view_data,
            on_close=mock_on_close,
            on_move_up=mock_on_move_up,
            on_move_down=mock_on_move_down,
        )

        # --- Test "Up" button for "Hammer" ---
        up_button = view._up_buttons["Hammer"]
        # The button's rect is relative to the view. The click event needs to be
        # in screen space.
        click_pos = (
            up_button.rect.centerx + view.rect.x,
            up_button.rect.centery + view.rect.y,
        )
        down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
        )
        up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos}
        )

        view.handle_event(down_event)
        view.handle_event(up_event)

        mock_on_move_up.assert_called_once_with("Hammer")
        mock_on_move_down.assert_not_called()

        mock_on_move_up.reset_mock()

        # --- Test "Down" button for "IcePick" ---
        down_button = view._down_buttons["IcePick"]
        click_pos = (
            down_button.rect.centerx + view.rect.x,
            down_button.rect.centery + view.rect.y,
        )
        down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
        )
        up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos}
        )

        view.handle_event(down_event)
        view.handle_event(up_event)

        mock_on_move_down.assert_called_once_with("IcePick")
        mock_on_move_up.assert_not_called()
