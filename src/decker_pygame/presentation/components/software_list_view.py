"""This module defines the SoftwareListView, which displays loaded software."""

import pygame

from decker_pygame.settings import BLACK, RED


class SoftwareListView(pygame.sprite.Sprite):
    """A view that displays the list of loaded software.

    This is a placeholder container for now.

    Args:
        position (tuple[int, int]): The top-left corner of the view.
        size (tuple[int, int]): The width and height of the view.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, RED, self.image.get_rect(), 3)
        self.rect = self.image.get_rect(topleft=position)
