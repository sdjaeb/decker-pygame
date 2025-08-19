"""This module defines the MapView component."""

import pygame

from decker_pygame.settings import MAP_VIEW


class MapView(pygame.sprite.Sprite):
    """A sprite that displays a 2D map of nodes and connections.

    Ported from MapView.cpp/h.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner.
        size (tuple[int, int]): The (width, height) of the map view surface.
        nodes (dict[str, tuple[int, int]]): A dictionary mapping node IDs to their
            (x, y) coordinates.
        connections (list[tuple[str, str]]): A list of tuples, where each tuple is a
            pair of node IDs representing a connection.

    Attributes:
        image (pygame.Surface): The surface that represents the map view.
        rect (pygame.Rect): The rectangular area of the map view.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        nodes: dict[str, tuple[int, int]],
        connections: list[tuple[str, str]],
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self.update_map(nodes, connections)

    def update_map(
        self,
        nodes: dict[str, tuple[int, int]],
        connections: list[tuple[str, str]],
    ) -> None:
        """Redraws the map with new node and connection data."""
        self.image.fill(MAP_VIEW.background_color)

        for start_node, end_node in connections:
            if start_node in nodes and end_node in nodes:
                pygame.draw.line(
                    self.image,
                    MAP_VIEW.line_color,
                    nodes[start_node],
                    nodes[end_node],
                    MAP_VIEW.line_width,
                )

        for pos in nodes.values():
            pygame.draw.circle(
                self.image, MAP_VIEW.node_color, pos, MAP_VIEW.node_radius
            )
