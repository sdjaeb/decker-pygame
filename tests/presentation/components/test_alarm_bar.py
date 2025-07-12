import pygame
import pytest

from decker_pygame.presentation.components.alarm_bar import AlarmBar
from decker_pygame.settings import ALARM


@pytest.fixture
def alarm_bar_instance():
    """Fixture to create a default AlarmBar instance for tests."""
    pygame.init()
    bar = AlarmBar(position=(10, 20), width=200, height=20)
    yield bar
    pygame.quit()


class TestAlarmBar:
    """Tests for the AlarmBar component."""

    def test_initialization(self, alarm_bar_instance: AlarmBar):
        """Tests that the alarm bar initializes correctly as a sprite."""
        bar = alarm_bar_instance

        assert isinstance(bar, pygame.sprite.Sprite)
        assert bar.rect.topleft == (10, 20)
        assert bar.rect.size == (200, 20)
        assert bar._percentage == 0.0
        assert bar._color == ALARM.colors[0]

        # Check that it's initially transparent
        assert bar.image.get_at((5, 5)) == pygame.Color(0, 0, 0, 0)

    def test_update_state_normal(self, alarm_bar_instance: AlarmBar):
        """Tests updating the alarm level in a normal, non-crashing state."""
        bar = alarm_bar_instance

        bar.update_state(alert_level=50, is_crashing=False)

        assert bar._percentage == 50.0

        expected_index = int(0.5 * (len(ALARM.colors) - 1))
        expected_color = ALARM.colors[expected_index]
        assert bar._color == expected_color

        # Check rendering: pixel at 25% width should be bar color
        assert bar.image.get_at((49, 10)) == expected_color
        # Pixel at 75% width should be transparent
        assert bar.image.get_at((151, 10)) == pygame.Color(0, 0, 0, 0)

    def test_update_state_crashing(self, alarm_bar_instance: AlarmBar):
        """Tests the alarm bar in a crashing state."""
        bar = alarm_bar_instance

        bar.update_state(alert_level=75, is_crashing=True)

        assert bar._percentage == 75.0
        assert bar._color == ALARM.crash_color
        assert bar.image.get_at((74, 10)) == ALARM.crash_color

    def test_alarm_level_clamping(self, alarm_bar_instance: AlarmBar):
        """Tests that the alarm level is clamped between 0 and 100."""
        bar = alarm_bar_instance

        bar.update_state(alert_level=150, is_crashing=False)
        assert bar._percentage == 100.0

        bar.update_state(alert_level=-50, is_crashing=False)
        assert bar._percentage == 0.0

    def test_alarm_bar_eq_and_hash_repr(self):
        """Tests basic object methods for the sprite."""
        pygame.init()
        bar1 = AlarmBar(position=(0, 0), width=100, height=10)
        bar2 = AlarmBar(position=(0, 0), width=100, height=10)

        assert bar1 == bar1
        assert bar1 != bar2  # Different object instances
        assert isinstance(hash(bar1), int)
        assert isinstance(repr(bar1), str)
        pygame.quit()
