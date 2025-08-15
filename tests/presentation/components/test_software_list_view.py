"""Tests for the SoftwareListView component."""

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
    view = SoftwareListView(position=(10, 20), size=(100, 200))
    assert view.rect.topleft == (10, 20)
    assert view.rect.size == (100, 200)
