"""This module defines the HealthBar component for the main game UI."""

from decker_pygame.presentation.components.percentage_bar import PercentageBar
from decker_pygame.settings import HEALTH


class HealthBar(PercentageBar):
    """A sprite component that displays a health value as a percentage bar.

    Args:
        position (tuple[int, int]): The top-left corner of the bar.
        width (int): The maximum width of the bar.
        height (int): The height of the bar.
    """

    def __init__(self, position: tuple[int, int], width: int, height: int):
        super().__init__(
            position=position,
            width=width,
            height=height,
            initial_color=HEALTH.colors[0][1],
        )
        self.update()

    def update_health(self, current: int, maximum: int) -> None:
        """Update the health bar's state based on current and max health values."""
        self._percentage = (current / maximum) * 100 if maximum > 0 else 0
        self._percentage = max(0, min(self._percentage, 100))

        # Default to the last color in the list (lowest health color) and then
        # find the first threshold that the health is greater than.
        if HEALTH.colors:
            self._color = HEALTH.colors[-1][1]
            for threshold, color in HEALTH.colors:
                if self._percentage > threshold:
                    self._color = color
                    break
        self.update()
