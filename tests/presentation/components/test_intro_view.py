from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.intro_view import IntroView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_intro_view_initialization():
    """Tests that the IntroView initializes and creates its content."""
    mock_on_continue = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.intro_view.Button"
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

        view = IntroView(on_continue=mock_on_continue)

        assert view is not None
        # 10 lines of text (including blank lines)
        assert mock_font_instance.render.call_count == 10
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]
        assert "Welcome to Decker." in rendered_texts
        assert "Your story begins now." in rendered_texts

        # 1 button should be created
        mock_button_class.assert_called_once()
        button_call = mock_button_class.call_args
        assert button_call.kwargs["text"] == "Continue"
        assert button_call.kwargs["on_click"] == mock_on_continue


def test_intro_view_event_handling():
    """Tests that the view correctly delegates events to its components."""
    mock_on_continue = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.intro_view.Button"
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

        view = IntroView(on_continue=mock_on_continue)

        with patch.object(
            view._components.sprites()[0], "handle_event"
        ) as mock_button_handler:
            event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}
            )
            view.handle_event(event)
            mock_button_handler.assert_called_once()
