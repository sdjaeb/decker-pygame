import uuid
from unittest.mock import call

from pytest_mock import MockerFixture

from decker_pygame.domain.events import PlayerCreated
from decker_pygame.domain.ids import PlayerId
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
    mock_dispatcher_class = mocker.patch(
        "decker_pygame.presentation.main.EventDispatcher"
    )
    mock_log_handler = mocker.patch(
        "decker_pygame.presentation.main.log_player_created"
    )
    mock_special_log_handler = mocker.patch(
        "decker_pygame.presentation.main.log_special_player_created"
    )
    mock_condition = mocker.patch("decker_pygame.presentation.main.is_special_player")

    # Configure the mock service's return values to be predictable
    mock_service_instance = mock_service_class.return_value
    deckard_player_id = PlayerId(uuid.uuid4())
    rynn_player_id = PlayerId(uuid.uuid4())
    mock_service_instance.create_new_player.side_effect = [
        deckard_player_id,
        rynn_player_id,
    ]

    # Call the main function
    main()

    # Assert that the infrastructure and application layers were wired correctly
    mock_repo_class.assert_called_once()
    mock_dispatcher_class.assert_called_once()

    mock_service_class.assert_called_once_with(
        player_repo=mock_repo_class.return_value,
        event_dispatcher=mock_dispatcher_class.return_value,
    )
    create_calls = [call(name="Deckard"), call(name="Rynn")]
    mock_service_instance.create_new_player.assert_has_calls(
        create_calls, any_order=False
    )

    subscribe_calls = [
        call(PlayerCreated, mock_log_handler),
        call(
            PlayerCreated,
            mock_special_log_handler,
            condition=mock_condition,
        ),
    ]
    mock_dispatcher_class.return_value.subscribe.assert_has_calls(
        subscribe_calls, any_order=True
    )

    # Assert that the presentation layer was composed and run
    mock_game_class.assert_called_once_with(
        player_service=mock_service_instance, player_id=deckard_player_id
    )
    mock_game_class.return_value.run.assert_called_once()
