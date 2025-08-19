"""This module defines the SoftwareListView, which displays loaded software."""

import pygame

from decker_pygame.settings import UI_FACE, UI_FONT


class SoftwareListView(pygame.sprite.Sprite):
    """A view that displays the list of loaded software.

    Args:
        position (tuple[int, int]): The top-left corner of the view.
        size (tuple[int, int]): The width and height of the view.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)
        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._software_list: list[str] = []

    def set_software(self, software: list[str]) -> None:
        """Sets the list of software to display."""
        self._software_list = software

    def update(self) -> None:
        """Redraws the list of software onto the component's surface."""
        self.image.fill((0, 0, 0, 0))  # Clear with transparent
        y_offset = 5
        for item in self._software_list:
            text_surface = self._font.render(item, True, UI_FACE)
            self.image.blit(text_surface, (5, y_offset))
            y_offset += self._font.get_height() + 2
