from unittest.mock import MagicMock, patch

import pygame
from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.components.alarm_bar import AlarmBar
from decker_pygame.game import Game
from decker_pygame.settings import ALARM


def test_game_run_loop_quits():
    """
    Tests that the main game loop runs and can be exited via a QUIT event.
    This test specifically covers the main `while` loop in the `run` method,
    which is often missed by component-level unit tests.
    """
    # Mock pygame.event.get to return a QUIT event on the first call.
    # The loop will process this, set is_running to False, and terminate.
    mock_event_get = MagicMock(return_value=[pygame.event.Event(pygame.QUIT)])

    # To properly unit test the Game class, we mock its direct dependencies
    # (the components it creates and functions it calls) rather than low-level
    # pygame functions. This isolates the Game logic from rendering and asset
    # loading, making the test more robust and focused.
    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode"),
        patch("decker_pygame.game.load_spritesheet", return_value=([], [])),
        patch("decker_pygame.game.ActiveBar", spec=ActiveBar),
        patch("decker_pygame.game.AlarmBar", spec=AlarmBar),
        patch("pygame.event.get", mock_event_get),
        patch("pygame.time.Clock"),
        patch(
            "pygame.display.flip"  # Mock flip to avoid video system errors
        ),
    ):
        game = Game()
        # The __init__ method sets this to True.
        assert game.is_running is True

        # The loop should run once, process the QUIT event, and terminate.
        game.run()

        # After the loop, is_running should be False.
        assert game.is_running is False
        mock_event_get.assert_called_once()


def test_game_update_cycles_alarm():
    """Tests that the temporary alarm cycling logic in _update works correctly."""
    # We need to mock get_ticks to control time.
    mock_ticks = MagicMock()

    with (
        patch("pygame.init"),
        patch("pygame.display.set_mode"),
        patch("decker_pygame.game.load_spritesheet", return_value=([], [])),
        patch("decker_pygame.game.ActiveBar", spec=ActiveBar),
        patch("decker_pygame.game.AlarmBar", spec=AlarmBar),
        patch("pygame.time.get_ticks", mock_ticks),
    ):
        # Initial state
        mock_ticks.return_value = 1000
        game = Game()
        assert game.alert_level == 0
        assert game.is_crashing is False

        # 1. Time hasn't passed enough, state should not change
        mock_ticks.return_value = 2000  # 1000ms passed
        game._update()
        assert game.alert_level == 0

        # 2. Time passes, alert level should increment
        mock_ticks.return_value = 4000  # 3000ms passed since init
        game._update()
        assert game.alert_level == 1

        # 3. Time passes again, alert level should increment to max
        mock_ticks.return_value = 7000  # another 3000ms
        game._update()
        assert game.alert_level == len(ALARM.colors) - 1

        # 4. At max alert, next update should trigger crashing
        mock_ticks.return_value = 10000
        game._update()
        assert game.is_crashing is True

        # 5. While crashing, next update should reset the alarm
        mock_ticks.return_value = 13000
        game._update()
        assert game.alert_level == 0
        assert game.is_crashing is False
