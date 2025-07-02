import os
import tempfile

from decker_pygame.application.services import PlayerService
from decker_pygame.infrastructure.persistence import JsonFilePlayerRepository
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

    # 2. Set up application services
    player_service = PlayerService(player_repo=player_repo)

    # 3. Create a player for the game session (example use case)
    player_id = player_service.create_new_player(name="Deckard")
    print(f"Initialized player {player_id} in {storage_path}")

    # 4. Compose and run the presentation layer, injecting dependencies
    game = Game(player_service=player_service, player_id=player_id)
    game.run()


if __name__ == "__main__":
    main()
