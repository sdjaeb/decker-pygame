"""This module defines the MessageView component for displaying text."""

import pygame

from decker_pygame.presentation.utils import render_text_wrapped
from decker_pygame.settings import UI_FONT


class MessageView(pygame.sprite.Sprite):
    """A sprite that displays multi-line text with word wrapping.

    Ported from MessageView.cpp/h.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner.
        size (tuple[int, int]): The (width, height) of the view's surface.
        background_color (pygame.Color): The background color for the text area.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        background_color: pygame.Color,
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._background_color = background_color
        self.font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self.font_color = UI_FONT.dark_font_color
        self.line_height = self.font.get_linesize()
        self.padding = 5

        self.image.fill(self._background_color)

    def set_text(self, text: str) -> None:
        """Renders the given text onto the view's surface with word wrapping."""
        self.image.fill(self._background_color)
        # The rect passed to the utility is the surface's own rect, with a 0,0 origin
        render_text_wrapped(
            surface=self.image,
            text=text,
            font=self.font,
            color=self.font_color,
            rect=self.image.get_rect(),
            padding=self.padding,
        )
