import uuid
from unittest.mock import ANY, call

from pytest_mock import MockerFixture

from decker_pygame.domain.character import Character
from decker_pygame.domain.events import ItemCrafted, PlayerCreated
from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId
from decker_pygame.presentation.main import main
from decker_pygame.settings import PATHS


def test_main_function(mocker: MockerFixture) -> None:
    """
    Test the main entry point function correctly wires up all layers
    and runs the game, without starting a real Pygame window.
    """
    # Patch all dependencies within the main module
    mock_pygame_init = mocker.patch("decker_pygame.presentation.main.pygame.init")
    mock_repo_class = mocker.patch(
        "decker_pygame.presentation.main.JsonFilePlayerRepository"
    )
    mock_char_repo_class = mocker.patch(
        "decker_pygame.presentation.main.JsonFileCharacterRepository"
    )
    mock_contract_repo_class = mocker.patch(
        "decker_pygame.presentation.main.JsonFileContractRepository"
    )
    mock_deck_repo_class = mocker.patch(
        "decker_pygame.presentation.main.JsonFileDeckRepository"
    )
    mock_deck_service_class = mocker.patch(
        "decker_pygame.presentation.main.DeckService"
    )
    mock_char_service_class = mocker.patch(
        "decker_pygame.presentation.main.CharacterService"
    )
    mock_contract_service_class = mocker.patch(
        "decker_pygame.presentation.main.ContractService"
    )
    mock_player_service_class = mocker.patch(
        "decker_pygame.presentation.main.PlayerService"
    )
    mock_crafting_service_class = mocker.patch(
        "decker_pygame.presentation.main.CraftingService"
    )
    mock_game_class = mocker.patch("decker_pygame.presentation.main.Game")
    mock_dispatcher_class = mocker.patch(
        "decker_pygame.presentation.main.EventDispatcher"
    )
    mock_logging_service_class = mocker.patch(
        "decker_pygame.presentation.main.LoggingService"
    )
    mock_console_writer_class = mocker.patch(
        "decker_pygame.presentation.main.ConsoleLogWriter"
    )
    mock_event_handler_factory = mocker.patch(
        "decker_pygame.presentation.main.create_event_logging_handler"
    )
    mock_special_log_handler = mocker.patch(
        "decker_pygame.presentation.main.log_special_player_created"
    )
    mock_condition = mocker.patch("decker_pygame.presentation.main.is_special_player")
    mock_character_create = mocker.patch(
        "decker_pygame.presentation.main.Character.create"
    )

    # Configure the mock service's return values to be predictable
    mock_player_service_instance = mock_player_service_class.return_value
    deckard_player_id = PlayerId(uuid.uuid4())
    rynn_player_id = PlayerId(uuid.uuid4())
    mock_player_service_instance.create_new_player.side_effect = [
        deckard_player_id,
        rynn_player_id,
    ]
    mock_deck_service_instance = mock_deck_service_class.return_value
    mock_deck_id = DeckId(uuid.uuid4())
    mock_deck_service_instance.create_deck.return_value = mock_deck_id

    # Configure the mock character that will be returned by the factory
    mock_character = mock_character_create.return_value
    mock_character.id = CharacterId(uuid.uuid4())

    # Call the main function
    main()

    # Assert that the infrastructure and application layers were wired correctly
    mock_repo_class.assert_called_once_with(base_path=PATHS.players_data)
    mock_char_repo_class.assert_called_once_with(base_path=PATHS.characters_data)
    mock_dispatcher_class.assert_called_once()
    mock_logging_service_class.assert_called_once_with(
        writers=[mock_console_writer_class.return_value]
    )
    mock_contract_repo_class.assert_called_once_with(base_path=PATHS.contracts_data)
    mock_deck_repo_class.assert_called_once_with(base_path=PATHS.decks_data)

    mock_player_service_class.assert_called_once_with(
        player_repo=mock_repo_class.return_value,
        event_dispatcher=mock_dispatcher_class.return_value,
    )
    mock_char_service_class.assert_called_once_with(
        character_repo=mock_char_repo_class.return_value,
        player_service=mock_player_service_class.return_value,
        event_dispatcher=mock_dispatcher_class.return_value,
    )
    mock_crafting_service_class.assert_called_once_with(
        character_repo=mock_char_repo_class.return_value,
        event_dispatcher=mock_dispatcher_class.return_value,
    )
    mock_deck_service_class.assert_called_once_with(
        deck_repo=mock_deck_repo_class.return_value,
        event_dispatcher=mock_dispatcher_class.return_value,
        character_repo=mock_char_repo_class.return_value,
    )

    create_calls = [call(name="Deckard"), call(name="Rynn")]
    mock_player_service_instance.create_new_player.assert_has_calls(
        create_calls, any_order=False
    )

    # Assert character creation and saving
    mock_character_create.assert_called_once_with(
        character_id=ANY,
        name="Rynn",
        deck_id=mock_deck_id,
        initial_skills={"crafting": 5},
        initial_credits=2000,
        initial_skill_points=5,
    )
    mock_char_repo_class.return_value.save.assert_called_once_with(mock_character)

    mock_event_handler_factory.assert_called_once_with(
        mock_logging_service_class.return_value
    )
    subscribe_calls = [
        call(PlayerCreated, mock_event_handler_factory.return_value),
        call(ItemCrafted, mock_event_handler_factory.return_value),
        call(
            PlayerCreated,
            mock_special_log_handler,
            condition=mock_condition,
        ),
        call(ItemCrafted, ANY),
    ]
    mock_dispatcher_class.return_value.subscribe.assert_has_calls(
        subscribe_calls, any_order=True
    )

    # Assert that the presentation layer was composed and run
    mock_game_class.assert_called_once_with(
        player_service=mock_player_service_instance,
        player_id=deckard_player_id,
        character_service=mock_char_service_class.return_value,
        contract_service=mock_contract_service_class.return_value,
        crafting_service=mock_crafting_service_class.return_value,
        character_id=mock_character.id,
        deck_service=mock_deck_service_class.return_value,
        logging_service=mock_logging_service_class.return_value,
    )
    mock_game_class.return_value.run.assert_called_once()
    mock_pygame_init.assert_called_once()


def test_main_function_dev_mode(mocker: MockerFixture) -> None:
    """
    Tests that the main function correctly applies dev settings when enabled.
    """
    # Patch all dependencies to prevent side effects
    mocker.patch("decker_pygame.presentation.main.pygame.init")
    mocker.patch("decker_pygame.presentation.main.JsonFilePlayerRepository")
    mock_char_repo_class = mocker.patch(
        "decker_pygame.presentation.main.JsonFileCharacterRepository"
    )
    mocker.patch("decker_pygame.presentation.main.PlayerService")
    mocker.patch("decker_pygame.presentation.main.CraftingService")
    mocker.patch("decker_pygame.presentation.main.Game")
    mocker.patch("decker_pygame.presentation.main.EventDispatcher")
    mocker.patch("decker_pygame.presentation.main.LoggingService")
    mocker.patch("decker_pygame.presentation.main.ConsoleLogWriter")
    mocker.patch("decker_pygame.presentation.main.create_event_logging_handler")
    mocker.patch("decker_pygame.presentation.main.log_special_player_created")
    mocker.patch("decker_pygame.presentation.main.is_special_player")
    mock_character_create = mocker.patch(
        "decker_pygame.presentation.main.Character.create"
    )

    # Enable dev mode for this test
    mocker.patch("decker_pygame.presentation.main.DEV_SETTINGS.enabled", True)

    # Configure a mock character to be returned by the factory
    mock_character = mocker.Mock(spec=Character)
    mock_character.credits = 2000
    mock_character.schematics = []
    mock_character_create.return_value = mock_character

    # Act
    main()

    # Assert that the character was modified by the dev-mode logic before saving
    assert mock_character.credits == 7000  # 2000 initial + 5000 debug
    assert len(mock_character.schematics) == 2  # The initial one + the debug one
    mock_char_repo_class.return_value.save.assert_called_once_with(mock_character)
