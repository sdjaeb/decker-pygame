import os
import tempfile
import uuid

from decker_pygame.application.crafting_service import CraftingService
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.application.event_handlers import (
    is_special_player,
    log_player_created,
    log_special_player_created,
)
from decker_pygame.application.player_service import PlayerService
from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.events import ItemCrafted, PlayerCreated
from decker_pygame.domain.ids import CharacterId
from decker_pygame.infrastructure.json_character_repository import (
    JsonFileCharacterRepository,
)
from decker_pygame.infrastructure.json_player_repository import JsonFilePlayerRepository
from decker_pygame.presentation.game import Game


def main() -> None:
    """
    Main entry point for the game.
    This is the "Composition Root" where we wire up our dependencies.
    """
    print("--- Decker Game Initializing ---")

    # 1. Set up infrastructure
    storage_path = os.path.join(tempfile.gettempdir(), "decker_pygame")
    player_repo = JsonFilePlayerRepository(base_path=storage_path)
    character_repo = JsonFileCharacterRepository(base_path=storage_path)
    event_dispatcher = EventDispatcher()

    # 2. Set up application services
    player_service = PlayerService(
        player_repo=player_repo, event_dispatcher=event_dispatcher
    )
    crafting_service = CraftingService(
        character_repo=character_repo, event_dispatcher=event_dispatcher
    )

    event_dispatcher.subscribe(PlayerCreated, log_player_created)
    event_dispatcher.subscribe(
        PlayerCreated,
        log_special_player_created,
        condition=is_special_player,
    )

    # 3. Create game entities for the session (example use case)
    player_id = player_service.create_new_player(name="Deckard")
    print(f"Initialized player {player_id} in {storage_path}")
    # Create a second player that will trigger the conditional handler
    player_service.create_new_player(name="Rynn")

    # Create a character and give them a schematic to test with
    character_id = CharacterId(uuid.uuid4())
    character = Character.create(
        character_id=character_id,
        name="Rynn",
        initial_skills={"crafting": 5},
        initial_credits=2000,
    )
    schematic = Schematic(
        name="IcePick v1",
        produces_item_name="IcePick v1",
        cost=[RequiredResource(name="credits", quantity=500)],
    )
    character.schematics.append(schematic)
    character_repo.save(character)
    print(f"Initialized character {character_id} in {storage_path}")

    # 4. Compose the presentation layer, injecting dependencies
    game = Game(
        player_service=player_service,
        player_id=player_id,
        crafting_service=crafting_service,
        character_id=CharacterId(character.id),
    )

    # 5. Wire up event handlers that depend on the presentation layer
    event_dispatcher.subscribe(
        ItemCrafted,
        lambda event: game.show_message(f"Successfully crafted {event.item_name}!"),
    )

    # 6. Run the game
    game.run()


if __name__ == "__main__":
    main()
