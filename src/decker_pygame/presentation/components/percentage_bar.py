"""This module provides a base class for percentage-based UI bars."""

import pygame


class PercentageBar(pygame.sprite.Sprite):
    """A base class for UI components that display a value as a.

    horizontal percentage bar.

    Args:
        position (tuple[int, int]): The top-left corner of the bar.
        width (int): The maximum width of the bar.
        height (int): The height of the bar.
        initial_color (pygame.Color): The initial color of the bar.

    Attributes:
        image (pygame.Surface): The surface that represents the bar.
        rect (pygame.Rect): The rectangular area of the bar.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        position: tuple[int, int],
        width: int,
        height: int,
        initial_color: pygame.Color,
    ) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

        self._percentage = 100.0
        self._color = initial_color

    def update(self) -> None:
        """Redraws the bar surface based on the current percentage and color."""
        self.image.fill((0, 0, 0, 0))  # Fill with a transparent color
        current_width = int(self.width * (self._percentage / 100))
        if current_width > 0:
            bar_rect = pygame.Rect(0, 0, current_width, self.height)
            pygame.draw.rect(self.image, self._color, bar_rect)
