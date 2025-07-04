import json
import os

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player
from decker_pygame.domain.player_repository_interface import PlayerRepositoryInterface


class JsonFilePlayerRepository(PlayerRepositoryInterface):
    """
    A concrete repository that persists Player aggregates to JSON files.
    Each player is stored in a separate file named after its ID.
    """

    def __init__(self, base_path: str) -> None:
        """
        Initialize the repository with a base directory for storage.

        Args:
            base_path (str): Directory where player files are stored.
        """
        self._base_path = base_path
        os.makedirs(self._base_path, exist_ok=True)

    def _get_path(self, player_id: PlayerId) -> str:
        """
        Return the file path for a given player ID.

        Args:
            player_id (PlayerId): The ID of the player.

        Returns:
            str: The file path for the player's JSON file.
        """
        return os.path.join(self._base_path, f"{player_id}.json")

    def save(self, player: Player) -> None:
        """
        Save a Player aggregate to a JSON file.

        Args:
            player (Player): The player aggregate to save.
        """
        player_dict = {
            "id": str(player.id),
            "name": player.name,
            "health": player.health,
        }
        with open(self._get_path(PlayerId(player.id)), "w") as f:
            json.dump(player_dict, f, indent=4)

    def get(self, player_id: PlayerId) -> Player | None:
        """
        Retrieve a Player aggregate from a JSON file, or None if not found.

        Args:
            player_id (PlayerId): The ID of the player to retrieve.

        Returns:
            Player | None: The player aggregate, or None if not found.
        """
        filepath = self._get_path(player_id)
        if not os.path.exists(filepath):
            return None

        with open(filepath) as f:
            data = json.load(f)

        # Reconstitute the aggregate directly from its data.
        # This is a key DDD concept: repositories restore objects to their
        # last known state without running business logic (which is in factories
        # or methods).
        return Player(id=player_id, name=data["name"], health=data["health"])
