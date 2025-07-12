"""This module defines the MapView component."""

import pygame

from decker_pygame.settings import MAP_VIEW


class MapView(pygame.sprite.Sprite):
    """A sprite that displays a 2D map of nodes and connections.

    Ported from MapView.cpp/h.
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
        """Initialize the MapView.

        Args:
            position: The (x, y) position of the top-left corner.
            size: The (width, height) of the map view surface.
            nodes: A dictionary mapping node IDs to their (x, y) coordinates.
            connections: A list of tuples, where each tuple is a pair of
                         node IDs representing a connection.
        """
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)

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
