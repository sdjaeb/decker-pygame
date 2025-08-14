"""The main entry point for the Decker-Pygame application.

This module serves as the Composition Root of the application. It is responsible
for initializing all layers of the architecture (infrastructure, application,
presentation), wiring up their dependencies, and starting the main game loop.
"""

import os
import tempfile
import uuid
from pathlib import Path

import pygame

from decker_pygame.application.character_service import CharacterService
from decker_pygame.application.contract_service import ContractService
from decker_pygame.application.crafting_service import CraftingService
from decker_pygame.application.deck_service import DeckService
from decker_pygame.application.domain_event_handlers import (
    create_event_logging_handler,
    is_special_player,
    log_special_player_created,
)
from decker_pygame.application.ds_file_service import DSFileService
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.application.logging_service import ConsoleLogWriter, LoggingService
from decker_pygame.application.node_service import NodeService
from decker_pygame.application.player_service import PlayerService
from decker_pygame.application.project_service import ProjectService
from decker_pygame.application.settings_service import SettingsService
from decker_pygame.application.shop_service import ShopService
from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.events import ItemCrafted, PlayerCreated
from decker_pygame.domain.ids import CharacterId, SchematicId
from decker_pygame.domain.project import ProjectType
from decker_pygame.infrastructure.json_character_repository import (
    JsonFileCharacterRepository,
)
from decker_pygame.infrastructure.json_contract_repository import (
    JsonFileContractRepository,
)
from decker_pygame.infrastructure.json_deck_repository import (
    JsonFileDeckRepository,
)
from decker_pygame.infrastructure.json_ds_file_repository import (
    JsonFileDSFileRepository,
)
from decker_pygame.infrastructure.json_player_repository import JsonFilePlayerRepository
from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.game import Game
from decker_pygame.settings import (
    DEV_SETTINGS,
    PATHS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)


def main() -> None:
    """Main entry point for the game.

    This is the "Composition Root" where we wire up our dependencies.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    print("--- Decker Game Initializing ---")

    # 1. Set up infrastructure
    storage_path = os.path.join(tempfile.gettempdir(), "decker_pygame")
    character_repo = JsonFileCharacterRepository(base_path=PATHS.characters_data)
    player_repo = JsonFilePlayerRepository(base_path=PATHS.players_data)
    contract_repo = JsonFileContractRepository(base_path=PATHS.contracts_data)
    deck_repo = JsonFileDeckRepository(base_path=PATHS.decks_data)
    ds_file_repo = JsonFileDSFileRepository(file_path=PATHS.ds_files_data)
    event_dispatcher = EventDispatcher()
    logging_service = LoggingService(writers=[ConsoleLogWriter()])
    asset_service = AssetService(
        assets_config_path=Path(PATHS.base_path) / "assets.json"
    )

    # 2. Set up application services
    player_service = PlayerService(
        player_repo=player_repo, event_dispatcher=event_dispatcher
    )
    character_service = CharacterService(
        character_repo=character_repo,
        player_service=player_service,
        event_dispatcher=event_dispatcher,
    )
    crafting_service = CraftingService(
        character_repo=character_repo, event_dispatcher=event_dispatcher
    )
    contract_service = ContractService(
        contract_repo=contract_repo, event_dispatcher=event_dispatcher
    )
    deck_service = DeckService(
        deck_repo=deck_repo,
        event_dispatcher=event_dispatcher,
        character_repo=character_repo,
    )
    ds_file_service = DSFileService(ds_file_repo=ds_file_repo)
    shop_service = ShopService(
        character_repo=character_repo,
    )
    node_service = NodeService()
    settings_service = SettingsService()
    project_service = ProjectService(
        character_repo=character_repo,
        event_dispatcher=event_dispatcher,
    )

    # 3. Set up generic event handlers
    event_logger = create_event_logging_handler(logging_service)
    event_dispatcher.subscribe(PlayerCreated, event_logger)
    event_dispatcher.subscribe(ItemCrafted, event_logger)
    event_dispatcher.subscribe(
        PlayerCreated,
        log_special_player_created,
        condition=is_special_player,
    )

    # 4. Create game entities for the session (example use case)
    player_id = player_service.create_new_player(name="Deckard")
    print(f"Initialized player {player_id} in {storage_path}")
    # Create a second player that will trigger the conditional handler
    player_service.create_new_player(name="Rynn")

    # Create a character and give them a schematic to test with
    character_id = CharacterId(uuid.uuid4())
    deck_id = deck_service.create_deck()
    character = Character.create(
        character_id=character_id,
        name="Rynn",
        deck_id=deck_id,
        initial_skills={"crafting": 5},
        initial_credits=2000,
        initial_skill_points=5,
        initial_reputation=0,
    )
    schematic = Schematic(
        id=SchematicId(uuid.uuid4()),
        type=ProjectType.SOFTWARE,
        name="IcePick v1",
        produces_item_name="IcePick v1",
        produces_item_size=10,
        rating=1,
        cost=[RequiredResource(name="credits", quantity=500)],
    )
    character.schematics.append(schematic)

    if DEV_SETTINGS.enabled:
        print("--- DEV MODE ENABLED: Applying debug settings. ---")
        # Give the character more money for testing shops
        character.credits += 5000
        # Add another schematic for testing crafting
        debug_schematic = Schematic(
            id=SchematicId(uuid.uuid4()),
            type=ProjectType.SOFTWARE,
            name="Debug Blaster",
            produces_item_name="Debug Blaster 9000",
            produces_item_size=50,
            rating=2,
            cost=[RequiredResource(name="credits", quantity=1)],
        )
        character.schematics.append(debug_schematic)

    character_repo.save(character)
    print(f"Initialized character {character_id} in {storage_path}")

    # 5. Compose the presentation layer, injecting dependencies
    game = Game(
        screen=screen,
        asset_service=asset_service,
        player_service=player_service,
        player_id=player_id,
        character_service=character_service,
        contract_service=contract_service,
        crafting_service=crafting_service,
        character_id=CharacterId(character.id),
        deck_service=deck_service,
        ds_file_service=ds_file_service,
        shop_service=shop_service,
        node_service=node_service,
        settings_service=settings_service,
        project_service=project_service,
        logging_service=logging_service,
    )

    # 6. Wire up event handlers that depend on the presentation layer
    event_dispatcher.subscribe(
        ItemCrafted,
        lambda event: game.show_message(f"Successfully crafted {event.item_name}!"),
    )

    # 7. Run the game
    game.run()


if __name__ == "__main__":
    main()
