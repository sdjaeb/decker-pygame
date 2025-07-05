from collections.abc import Generator
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.clock_view import ClockView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_font() -> Generator[Mock]:
    """Provides a mock pygame.font.Font instance."""
    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_class.return_value = mock_font_instance
        yield mock_font_instance


def test_initialization(mock_font: Mock):
    """Tests that the ClockView initializes and renders its initial text."""
    view = ClockView(position=(10, 10), initial_text="INIT")
    assert view.rect.topleft == (10, 10)
    mock_font.render.assert_called_once_with("INIT", True, view.color)


def test_set_text(mock_font: Mock):
    """Tests that the set_text method re-renders the text."""
    view = ClockView(position=(10, 10))
    mock_font.render.reset_mock()  # Reset mock from the __init__ call

    view.set_text("NEW TEXT")
    mock_font.render.assert_called_once_with("NEW TEXT", True, view.color)
