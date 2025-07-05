import pygame

from decker_pygame.settings import HEALTH


class HealthBar(pygame.sprite.Sprite):
    """A sprite component that displays a health value as a percentage bar."""

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], width: int, height: int):
        """
        Initialize the HealthBar.

        Args:
            position: The (x, y) position of the top-left corner.
            width: The maximum width of the bar.
            height: The height of the bar.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

        self._health_percent = 100.0
        self._color = HEALTH.colors[0][1]

        self.update()

    def update_health(self, current: int, maximum: int) -> None:
        """
        Update the health bar's state based on current and max health values.

        Args:
            current: The current health value.
            maximum: The maximum possible health value.
        """
        self._health_percent = (current / maximum) * 100 if maximum > 0 else 0
        self._health_percent = max(0, min(self._health_percent, 100))

        # Default to the last color in the list (lowest health color) and then
        # find the first threshold that the health is greater than.
        if HEALTH.colors:
            self._color = HEALTH.colors[-1][1]
            for threshold, color in HEALTH.colors:
                if self._health_percent > threshold:
                    self._color = color
                    break
        self.update()

    def update(self) -> None:
        """Redraws the health bar surface based on the current state."""
        self.image.fill((0, 0, 0, 0))  # Fill with a transparent color
        current_width = int(self.width * (self._health_percent / 100))
        if current_width > 0:
            bar_rect = pygame.Rect(0, 0, current_width, self.height)
            pygame.draw.rect(self.image, self._color, bar_rect)
