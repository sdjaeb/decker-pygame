import pygame

from decker_pygame.components.alarm_bar import AlarmBar
from decker_pygame.settings import ALARM


class TestAlarmBar:
    def test_initialization_and_state_update(self):
        pygame.init()

        alarm_bar = AlarmBar(position=(10, 20))

        # Check position
        assert alarm_bar.rect.topleft == (10, 20)

        # Check dimensions
        assert alarm_bar.image.get_width() == ALARM.width
        assert alarm_bar.image.get_height() == ALARM.height

        # Check initial state (alert_level=0, is_crashing=False)
        assert alarm_bar.image.get_at((0, 0)) == ALARM.colors[0]

        # Test alert level 1
        alarm_bar.update_state(1, False)
        assert alarm_bar.image.get_at((0, 0)) == ALARM.colors[1]

        # Test alert level 2
        alarm_bar.update_state(2, False)
        assert alarm_bar.image.get_at((0, 0)) == ALARM.colors[2]

        # Test crashing state
        alarm_bar.update_state(0, True)
        assert alarm_bar.image.get_at((0, 0)) == ALARM.crash_color

        # Test alert level clamping (out of bounds high)
        alarm_bar.update_state(100, False)
        assert alarm_bar.image.get_at((0, 0)) == ALARM.colors[-1]

        pygame.quit()
