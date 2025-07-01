from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pygame
import pytest

from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.components.alarm_bar import AlarmBar
from decker_pygame.game import Game
from decker_pygame.settings import ALARM


@pytest.fixture
def mocked_game_instance() -> Generator[Game]:
    """
    Provides a fully mocked Game instance suitable for unit testing game logic
    without initializing pygame modules.
    """
    # Mock all external dependencies called in Game.__init__ and Game.run
    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.display.flip"),
        patch("pygame.time.Clock"),
        patch("pygame.time.get_ticks", return_value=0),  # Mock ticks during init
        patch("decker_pygame.game.load_spritesheet", return_value=([], [])),
        patch("decker_pygame.game.ActiveBar", spec=ActiveBar),
        patch("decker_pygame.game.AlarmBar", spec=AlarmBar),
    ):
        yield Game()


def test_game_run_loop_quits(mocked_game_instance: Game):
    """Tests that the main game loop runs and can be exited via a QUIT event."""
    game = mocked_game_instance
    # Mock event.get to return a QUIT event on the first call.
    with patch(
        "pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)]
    ) as mock_event_get:
        # The __init__ method sets this to True.
        assert game.is_running is True

        # The loop should run once, process the QUIT event, and terminate.
        game.run()

        assert game.is_running is False
        mock_event_get.assert_called_once()


def test_game_update_cycles_alarm(mocked_game_instance: Game):
    """Tests that the temporary alarm cycling logic in _update works correctly."""
    game = mocked_game_instance

    with patch("pygame.time.get_ticks", MagicMock()) as mock_ticks:
        # Initial state
        mock_ticks.return_value = 1000
        game.last_alarm_update = mock_ticks()  # Sync last_alarm_update
        assert game.alert_level == 0
        assert not game.is_crashing

        # 1. Time hasn't passed enough, state should not change
        mock_ticks.return_value = 2000  # 1000ms passed
        game._update()
        assert game.alert_level == 0

        # 2. Time passes threshold, alert level should increment
        mock_ticks.return_value = 4000  # 3000ms passed since init
        game._update()
        assert game.alert_level == 1

        # 3. Cycle through the remaining alert levels
        max_alert_index = len(ALARM.colors) - 1
        for i in range(2, max_alert_index + 1):
            mock_ticks.return_value += 3000  # Advance time
            game._update()
            assert game.alert_level == i, f"Failed at alert level {i}"

        # 4. At max alert, next update should trigger crashing
        assert game.alert_level == max_alert_index
        mock_ticks.return_value += 3000
        game._update()
        assert game.is_crashing is True
        assert game.alert_level == max_alert_index

        # 5. While crashing, next update should reset the alarm
        mock_ticks.return_value += 3000
        game._update()
        assert game.alert_level == 0
        assert game.is_crashing is False
