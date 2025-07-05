import pygame

from decker_pygame.settings import ALARM


class AlarmBar(pygame.sprite.Sprite):
    """
    A sprite component that displays the system alert level as a percentage bar.
    The bar's color changes as the alert level increases.
    """

    image: pygame.Surface
    rect: pygame.Rect
    alarm_level: int
    color: pygame.Color

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Initialize the AlarmBar.

        Args:
            position: The (x, y) position of the top-left corner of the bar.
            width: The maximum width of the bar.
            height: The height of the bar.
        """
        super().__init__()

        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.alarm_level = 0
        self.color = ALARM.colors[0]

        self.update()  # Initial draw

    def update_state(self, alert_level: int, is_crashing: bool) -> None:
        """
        Update the alarm bar's state and color based on the alert level.

        Args:
            alert_level: The new alarm level (0-100).
            is_crashing: Whether the system is crashing.
        """
        self.alarm_level = max(0, min(alert_level, 100))

        if is_crashing:
            self.color = ALARM.crash_color
        else:
            num_colors = len(ALARM.colors)
            if num_colors > 0:
                index = int((self.alarm_level / 100) * (num_colors - 1))
                self.color = ALARM.colors[index]

        self.update()

    def update(self) -> None:
        """Redraws the alarm bar surface based on the current state."""
        self.image.fill((0, 0, 0, 0))  # Fill with a transparent color
        current_width = int(self.width * (self.alarm_level / 100))
        if current_width > 0:
            bar_rect = pygame.Rect(0, 0, current_width, self.height)
            pygame.draw.rect(self.image, self.color, bar_rect)
