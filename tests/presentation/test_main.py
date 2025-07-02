from pytest_mock import MockerFixture

from decker_pygame.presentation.main import main


def test_main_function(mocker: MockerFixture) -> None:
    """
    Test the main entry point function correctly wires up all layers
    and runs the game, without starting a real Pygame window.
    """
    # Patch all dependencies within the main module
    mock_repo_class = mocker.patch(
        "decker_pygame.presentation.main.JsonFilePlayerRepository"
    )
    mock_service_class = mocker.patch("decker_pygame.presentation.main.PlayerService")
    mock_game_class = mocker.patch("decker_pygame.presentation.main.Game")

    # Call the main function
    main()

    # Assert that the infrastructure and application layers were wired correctly
    mock_repo_class.assert_called_once()
    mock_service_class.assert_called_once_with(player_repo=mock_repo_class.return_value)
    mock_service_class.return_value.create_new_player.assert_called_once_with(
        name="Deckard"
    )

    # Assert that the presentation layer was composed and run
    mock_game_class.assert_called_once()
    mock_game_class.return_value.run.assert_called_once()
