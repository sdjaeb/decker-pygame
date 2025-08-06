from unittest.mock import ANY, Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import IceDataViewDTO
from decker_pygame.presentation.components.ice_data_view import IceDataView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_ice_data_view_initialization_and_rendering():
    """Tests that the IceDataView initializes and renders its data correctly."""
    mock_on_close = Mock()
    view_data = IceDataViewDTO(
        name="Black ICE",
        ice_type="Barrier",
        strength=8,
        description="A tough defensive program.",
        cost=2500,
    )

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.ice_data_view.Button"
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        view = IceDataView(data=view_data, on_close=mock_on_close)

        assert view is not None
        # Title + 4 data lines
        assert mock_font_instance.render.call_count == 5
        rendered_texts = {
            call.args[0] for call in mock_font_instance.render.call_args_list
        }
        assert "Black ICE" in rendered_texts
        assert "Type: Barrier" in rendered_texts
        assert "Strength: 8" in rendered_texts
        assert "Cost: $2500" in rendered_texts
        assert "Description: A tough defensive program." in rendered_texts

        mock_button_class.assert_called_once_with(
            position=ANY, size=ANY, text="Close", on_click=mock_on_close
        )


def test_ice_data_view_delegates_close_event():
    """Tests that clicking the close button triggers the on_close callback."""
    mock_on_close = Mock()
    view_data = IceDataViewDTO(
        name="Black ICE", ice_type="Barrier", strength=8, description="...", cost=2500
    )

    with patch("pygame.font.Font") as mock_font_class:
        # Use a real button to test the click
        # We must configure the mock font to return a real surface to avoid a
        # TypeError when the Button tries to blit the rendered text.
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((10, 10))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance
        view = IceDataView(data=view_data, on_close=mock_on_close)

        close_button = view._close_button
        click_pos = (
            close_button.rect.centerx + view.rect.x,
            close_button.rect.centery + view.rect.y,
        )
        down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
        )
        up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos}
        )

        view.handle_event(down_event)
        view.handle_event(up_event)

        mock_on_close.assert_called_once()
