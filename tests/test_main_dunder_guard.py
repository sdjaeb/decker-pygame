def test_main_dunder_guard() -> None:
    """
    Test that the script runs via the `if __name__ == '__main__'` guard
    without executing the real game loop.
    """
    import runpy
    import sys
    from unittest.mock import Mock, patch

    # Create a mock Game class that has a mock `run` method.
    mock_run = Mock()
    mock_game_instance = Mock(run=mock_run)
    mock_game_class = Mock(return_value=mock_game_instance)

    # The key is to patch `Game` where it is defined (`decker_pygame.game`).
    # When `runpy` executes `main.py`, the line `from decker_pygame.game import Game`
    # will then import our mock instead of the real one. This avoids the
    # infinite loop in the real Game.run() method.
    with patch("decker_pygame.game.Game", mock_game_class):
        # We must ensure that runpy performs a fresh import of the modules.
        if "decker_pygame.main" in sys.modules:
            del sys.modules["decker_pygame.main"]
        runpy.run_module("decker_pygame.main", run_name="__main__")

    mock_game_class.assert_called_once()
    mock_run.assert_called_once()
