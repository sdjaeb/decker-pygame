import pygame
import pytest

from decker_pygame.presentation.components.map_view import MapView
from decker_pygame.settings import MAP_VIEW


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def map_data():
    """Provides sample node and connection data for map tests."""
    nodes = {"A": (30, 30), "B": (100, 80), "C": (50, 120)}
    connections = [("A", "B")]  # C is not connected
    return nodes, connections


def test_map_view_rendering(map_data):
    """Tests that the MapView correctly renders nodes and connections."""
    nodes, connections = map_data
    view = MapView(
        position=(0, 0), size=(200, 150), nodes=nodes, connections=connections
    )

    # Check that a pixel at a node's center has the node color
    assert view.image.get_at(nodes["A"]) == MAP_VIEW.node_color
    assert view.image.get_at(nodes["B"]) == MAP_VIEW.node_color
    assert view.image.get_at(nodes["C"]) == MAP_VIEW.node_color

    # Check that a pixel on the line has the line color
    mid_x = (nodes["A"][0] + nodes["B"][0]) // 2
    mid_y = (nodes["A"][1] + nodes["B"][1]) // 2
    assert view.image.get_at((mid_x, mid_y)) == MAP_VIEW.line_color

    # Check that a pixel on the background has the background color
    assert view.image.get_at((1, 1)) == MAP_VIEW.background_color
