"""Tests for the NodeGridView component."""

import pygame
import pytest

from decker_pygame.presentation.components.node_grid_view import NodeGridView


@pytest.fixture(autouse=True)
def pygame_init_fixture():
    """Fixture to initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_node_grid_view_initialization():
    """Tests that the NodeGridView initializes with the correct position and size."""
    view = NodeGridView(position=(10, 20), size=(100, 200))
    assert view.rect.topleft == (10, 20)
    assert view.rect.size == (100, 200)
