"""This module defines a simple Label component for displaying text."""

import pygame
from pygame.color import Color


class Label(pygame.sprite.Sprite):
    """A non-interactive sprite that displays a single line of text.

    Attributes:
        image (pygame.Surface): The surface that represents the label.
        rect (pygame.Rect): The rectangular area of the label.

    Args:
        text (str): The text to display.
        position (tuple[int, int]): The top-left corner of the label.
        font (pygame.font.Font): The font to use for rendering.
        color (Color | str | tuple[int, ...]): The color of the text. Defaults to
            "white".
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        text: str,
        position: tuple[int, int],
        font: pygame.font.Font,
        color: Color | str | tuple[int, ...] = "white",
    ):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(topleft=position)
