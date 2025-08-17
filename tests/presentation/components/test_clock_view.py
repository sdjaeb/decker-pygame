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
    """Tests that the ClockView initializes and renders a zero time."""
    view = ClockView(position=(10, 10), size=(44, 11))
    assert view.rect.topleft == (10, 10)
    mock_font.render.assert_called_once_with("00:00:00", True, view.color)


def test_update_time(mock_font: Mock):
    """Tests that the update_time method correctly formats and renders the time."""
    view = ClockView(position=(10, 10), size=(44, 11))
    mock_font.render.reset_mock()  # Reset mock from the __init__ call

    view.update_time(3661)  # 1 hour, 1 minute, 1 second
    mock_font.render.assert_called_once_with("01:01:01", True, view.color)

    mock_font.render.reset_mock()
    view.update_time(59)  # 59 seconds
    mock_font.render.assert_called_once_with("00:00:59", True, view.color)
