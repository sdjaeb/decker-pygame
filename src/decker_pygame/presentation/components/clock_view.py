"""This module defines the ClockView component for the main game UI."""

import pygame

from decker_pygame.settings import RED, UI_FONT


class ClockView(pygame.sprite.Sprite):
    """A sprite component that displays text, intended for the game clock.

    This is a placeholder implementation that renders text. The original used
    a custom digit spritesheet. It takes a total number of seconds and formats
    it as HH:MM:SS.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner.
        size (tuple[int, int]): The (width, height) of the view.

    Attributes:
        image (pygame.Surface): The surface that represents the text.
        rect (pygame.Rect): The rectangular area of the text.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self.font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self.color = UI_FONT.default_font_color
        self.update_time(0)  # Initialize with zero time

    def update_time(self, total_seconds: int) -> None:
        """Update the displayed time from a total number of seconds.

        This formats the seconds into HH:MM:SS and redraws the sprite's image.

        Args:
            total_seconds (int): The total time in seconds to display.
        """
        # Add a background for development visibility
        self.image.fill(RED)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
        text_surface = self.font.render(time_string, True, self.color)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)
