import runpy
import sys
from unittest.mock import patch


def test_main_dunder_guard() -> None:
    """
    Test that running the module as a script executes the main function,
    which in turn runs the game.
    """
    # Patch Game at its source to prevent the real game loop from running.
    with patch("decker_pygame.presentation.game.Game") as mock_game:
        # Ensure a fresh import by runpy
        if "decker_pygame.presentation.main" in sys.modules:
            del sys.modules["decker_pygame.presentation.main"]

        # Run the module as if it were the main script
        runpy.run_module("decker_pygame.presentation.main", run_name="__main__")

    # Assert that the Game was instantiated and its run method was called.
    mock_game.assert_called_once()
    mock_game.return_value.run.assert_called_once()
