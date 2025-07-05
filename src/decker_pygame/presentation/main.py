import os
import tempfile

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.application.event_handlers import (
    is_special_player,
    log_player_created,
    log_special_player_created,
)
from decker_pygame.application.player_service import PlayerService
from decker_pygame.domain.events import PlayerCreated
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
    event_dispatcher = EventDispatcher()

    # 2. Set up application services
    player_service = PlayerService(
        player_repo=player_repo, event_dispatcher=event_dispatcher
    )

    event_dispatcher.subscribe(PlayerCreated, log_player_created)
    event_dispatcher.subscribe(
        PlayerCreated,
        log_special_player_created,
        condition=is_special_player,
    )

    # 3. Create a player for the game session (example use case)
    player_id = player_service.create_new_player(name="Deckard")
    print(f"Initialized player {player_id} in {storage_path}")
    # Create a second player that will trigger the conditional handler
    player_service.create_new_player(name="Rynn")

    # 4. Compose and run the presentation layer, injecting dependencies
    game = Game(player_service=player_service, player_id=player_id)
    game.run()


if __name__ == "__main__":
    main()
