from decker_pygame.presentation.components.percentage_bar import PercentageBar
from decker_pygame.settings import ALARM


class AlarmBar(PercentageBar):
    """
    A sprite component that displays the system alert level as a percentage bar.
    The bar's color changes as the alert level increases.
    """

    def __init__(self, position: tuple[int, int], width: int, height: int) -> None:
        """
        Initialize the AlarmBar.

        Args:
            position: The (x, y) position of the top-left corner.
            width: The maximum width of the bar.
            height: The height of the bar.
        """
        super().__init__(
            position=position,
            width=width,
            height=height,
            initial_color=ALARM.colors[0],
        )
        self._percentage = 0.0  # Alarm starts at 0
        self.update()  # Initial draw

    def update_state(self, alert_level: int, is_crashing: bool) -> None:
        """
        Update the alarm bar's state and color based on the alert level.

        Args:
            alert_level: The new alarm level (0-100).
            is_crashing: Whether the system is crashing.
        """
        self._percentage = float(max(0, min(alert_level, 100)))

        if is_crashing:
            self._color = ALARM.crash_color
        else:
            num_colors = len(ALARM.colors)
            if num_colors > 0:
                index = int((self._percentage / 100) * (num_colors - 1))
                self._color = ALARM.colors[index]

        self.update()
