"""This module defines the ImageDisplay component."""

import pygame


class ImageDisplay(pygame.sprite.Sprite):
    """A simple sprite that displays a single, static image.

    This is useful for backgrounds, logos, or other non-interactive elements.
    Ported from ImageDisplay.cpp/h.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner.
        image (pygame.Surface): The pygame.Surface to display.

    Attributes:
        image (pygame.Surface): The image being displayed.
        rect (pygame.Rect): The rectangular area of the image.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
