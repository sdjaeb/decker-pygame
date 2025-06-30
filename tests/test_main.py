from pytest_mock import MockerFixture

from decker_pygame.main import main


def test_main_function(mocker: MockerFixture) -> None:
    """Test the main entry point function creates and runs a Game."""
    # Patch the Game class where it is looked up (in the main module),
    # not where it is defined.
    mock_game_class = mocker.patch("decker_pygame.main.Game")
    main()
    mock_game_class.assert_called_once()
    mock_game_class.return_value.run.assert_called_once()
