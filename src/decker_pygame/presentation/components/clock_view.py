import pygame

from decker_pygame.settings import UI_FONT


class ClockView(pygame.sprite.Sprite):
    """A sprite component that displays text, intended for the game clock."""

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], initial_text: str = "00:00:00"):
        """
        Initialize the ClockView.

        Args:
            position: The (x, y) position of the top-left corner.
            initial_text: The text to display initially.
        """
        super().__init__()
        self.font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self.color = UI_FONT.default_font_color
        self.pos = position
        self.set_text(initial_text)

    def set_text(self, text: str) -> None:
        """
        Update the displayed text. This redraws the sprite's image.

        Args:
            text: The new text to display.
        """
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
