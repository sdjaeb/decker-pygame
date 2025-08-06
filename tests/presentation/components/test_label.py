"""Tests for the Label component."""

from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.components.label import Label


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_label_initialization():
    """Tests that the Label initializes and renders correctly."""
    mock_font = Mock(spec=pygame.font.Font)
    mock_surface = pygame.Surface((100, 20))
    mock_font.render.return_value = mock_surface

    label = Label(
        text="Test Label",
        position=(10, 20),
        font=mock_font,
        color="red",
    )

    assert label.rect.topleft == (10, 20)
    assert label.image is mock_surface
    mock_font.render.assert_called_once_with("Test Label", True, "red")
