"""This module defines the AlarmBar component for the main game UI."""

from decker_pygame.presentation.components.percentage_bar import PercentageBar
from decker_pygame.settings import ALARM


class AlarmBar(PercentageBar):
    """A sprite component that displays the system alert level as a percentage bar.

    The bar's color changes as the alert level increases.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner.
        width (int): The maximum width of the bar.
        height (int): The height of the bar.
    """

    def __init__(self, position: tuple[int, int], width: int, height: int) -> None:
        super().__init__(
            position=position,
            width=width,
            height=height,
            initial_color=ALARM.colors[0],
        )
        self._percentage = 0.0  # Alarm starts at 0, overriding parent

    def set_percentage(self, value: float) -> None:
        """Set the percentage and update the color accordingly."""
        super().set_percentage(value)

        # TODO: Add logic for is_crashing state when it's available in the DTO
        num_colors = len(ALARM.colors)
        if num_colors > 0:
            # Ensure index is within bounds
            index = int((self._percentage / 100) * (num_colors - 1))
            index = max(0, min(index, num_colors - 1))
            self._color = ALARM.colors[index]
