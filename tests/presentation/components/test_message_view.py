from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.message_view import MessageView


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


def test_message_view_handles_unbreakable_words(mock_font: Mock):
    """Tests that a word longer than the line width is forced to wrap."""
    bg_color = pygame.Color("black")
    # View width is 200, padding is 5, so max text width is 190.
    # font.size returns len * 10, so max line length is 19 chars.
    view = MessageView(position=(0, 0), size=(200, 100), background_color=bg_color)

    # This word is longer than 19 characters
    text_to_render = "A_very_long_unbreakable_word"
    view.set_text(text_to_render)

    # Check that font.render was called with the expected wrapped lines.
    rendered_lines = [call.args[0] for call in mock_font.render.call_args_list]
    assert rendered_lines[0] == "A_very_long_unbreak"
    assert rendered_lines[1] == "able_word"


def test_message_view_font_fallback_to_sysfont(mocker):
    """
    Tests that MessageView falls back to SysFont if pygame.font.Font fails.
    """
    # Arrange: Make the primary font loader fail
    mocker.patch("pygame.font.Font", side_effect=pygame.error("Cannot load font"))
    mock_sysfont = mocker.patch("pygame.font.SysFont", return_value=Mock())

    # Act
    view = MessageView(
        position=(0, 0), size=(100, 100), background_color=pygame.Color("black")
    )

    # Assert
    assert view.font is mock_sysfont.return_value
    mock_sysfont.assert_called_once()


def test_message_view_font_fallback_to_dummy(mocker):
    """
    Tests that MessageView falls back to a dummy font if all pygame fonts fail.
    """
    # Arrange: Make all pygame font loaders fail
    mocker.patch("pygame.font.Font", side_effect=pygame.error("Cannot load font"))
    mocker.patch("pygame.font.SysFont", side_effect=pygame.error("Cannot load sysfont"))

    # Act
    view = MessageView(
        position=(0, 0), size=(100, 100), background_color=pygame.Color("black")
    )
    view.set_text("test")  # This will call render on the dummy font

    # Assert
    assert view.font is not None
    # Check if it has the methods of our _DummyFont
    assert hasattr(view.font, "get_linesize")
    assert hasattr(view.font, "render")
