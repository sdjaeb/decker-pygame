from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.message_view import MessageView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_font() -> Generator[Mock]:
    """Provides a mock pygame.font.Font instance with a predictable size method."""
    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        # Make size() return the length of the string * 10 for width
        mock_font_instance.size.side_effect = lambda text: (len(text) * 10, 15)
        mock_font_instance.get_linesize.return_value = 18
        mock_font_instance.render.return_value = pygame.Surface((10, 10))
        mock_font_class.return_value = mock_font_instance
        yield mock_font_instance


def test_message_view_initialization(mock_font: Mock):
    """Tests that the MessageView initializes correctly."""
    bg_color = pygame.Color("black")
    view = MessageView(position=(10, 20), size=(200, 100), background_color=bg_color)

    assert view.rect.topleft == (10, 20)
    assert view.image.get_at((5, 5)) == bg_color


def test_message_view_word_wrapping(mock_font: Mock):
    """Tests that text is correctly word-wrapped and rendered."""
    bg_color = pygame.Color("black")
    # View width is 200, padding is 5, so max text width is 190.
    # font.size returns len * 10, so max line length is 19 chars.
    view = MessageView(position=(0, 0), size=(200, 100), background_color=bg_color)

    text_to_render = "This is a very long message to test the wrapping."
    view.set_text(text_to_render)

    # Check that font.render was called with the expected wrapped lines.
    rendered_lines = [call.args[0] for call in mock_font.render.call_args_list]
    assert rendered_lines[0] == "This is a very long"
    assert rendered_lines[1] == "message to test the"
    assert rendered_lines[2] == "wrapping."
