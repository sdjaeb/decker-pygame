from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import RestViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.rest_view import RestView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def rest_data():
    return RestViewData(cost=100, health_recovered=50)


def test_rest_view_initialization(rest_data):
    """Tests that the view initializes and renders data correctly."""
    mock_on_rest = Mock()
    mock_on_close = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.rest_view.Button"
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

        view = RestView(data=rest_data, on_rest=mock_on_rest, on_close=mock_on_close)

        assert view is not None
        # Title + 2 lines of data
        assert mock_font_instance.render.call_count == 3
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]

        assert "Cost to rest: $100" in rendered_texts
        assert "Health recovered: 50%" in rendered_texts

        assert mock_button_class.call_count == 2
        button_calls = mock_button_class.call_args_list
        button_texts = [call.kwargs["text"] for call in button_calls]
        button_callbacks = [call.kwargs["on_click"] for call in button_calls]
        assert "Rest" in button_texts
        assert "Cancel" in button_texts
        assert mock_on_rest in button_callbacks
        assert mock_on_close in button_callbacks


def test_rest_view_event_handling(rest_data):
    """Tests that the view correctly delegates events to its components."""
    mock_on_rest = Mock()
    mock_on_close = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.rest_view.Button"
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

        view = RestView(data=rest_data, on_rest=mock_on_rest, on_close=mock_on_close)

        # We can test the event delegation by checking if the button's method is called
        with patch.object(
            view._components.sprites()[0], "handle_event"
        ) as mock_button_handler:
            event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}
            )
            view.handle_event(event)
            mock_button_handler.assert_called_once()
