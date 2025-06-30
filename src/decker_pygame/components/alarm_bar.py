import pygame
from decker_pygame.settings import ALARM


class AlarmBar(pygame.sprite.Sprite):
    """A sprite that displays the system alert level."""

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface((ALARM.width, ALARM.height))
        self.rect = self.image.get_rect(topleft=position)
        # Set initial state
        self.update_state(0, False)

    def update_state(self, alert_level: int, is_crashing: bool) -> None:
        """Updates the bar's color based on game state."""
        if is_crashing:
            color = ALARM.crash_color
        else:
            # Clamp alert_level to be a valid index
            level = max(0, min(alert_level, len(ALARM.colors) - 1))
            color = ALARM.colors[level]
        self.image.fill(color)
