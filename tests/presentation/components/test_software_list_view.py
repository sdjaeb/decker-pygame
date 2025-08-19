"""Tests for the SoftwareListView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.software_list_view import SoftwareListView


@pytest.fixture(autouse=True)
def pygame_init_fixture():
    """Fixture to initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_software_list_view_initialization():
    """Tests that the SoftwareListView initializes the correct position and size."""
    with patch("pygame.font.Font"):
        view = SoftwareListView(position=(10, 20), size=(100, 200))
        assert view.rect.topleft == (10, 20)
        assert view.rect.size == (100, 200)
        assert view._software_list == []


def test_set_software():
    """Tests that set_software updates the internal list."""
    with patch("pygame.font.Font"):
        view = SoftwareListView(position=(10, 20), size=(100, 200))
        software = ["Program A", "Program B"]
        view.set_software(software)
        assert view._software_list == software


@patch("pygame.font.Font")
def test_update_renders_software_list(mock_font_class: Mock):
    """Tests that the update method renders the software list."""
    mock_font_instance = mock_font_class.return_value
    mock_font_instance.render.return_value = pygame.Surface((50, 10))
    mock_font_instance.get_height.return_value = 10

    view = SoftwareListView(position=(10, 20), size=(100, 200))
    software = ["Hammer v1", "IcePick v2"]
    view.set_software(software)

    view.update()

    assert mock_font_instance.render.call_count == 2
