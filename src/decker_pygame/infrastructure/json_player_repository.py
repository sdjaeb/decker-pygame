"""A JSON file-based implementation of the Player repository interface."""

import json
import os
from typing import Any

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player
from decker_pygame.ports.repository_interfaces import PlayerRepositoryInterface


class JsonFilePlayerRepository(PlayerRepositoryInterface):
    """A concrete repository that persists Player aggregates to JSON files.

    Each player is stored in a separate file named after its ID.

    Args:
        base_path (str): Directory where player files are stored.
    """

    def __init__(self, base_path: str) -> None:
        self._base_path = base_path
        os.makedirs(self._base_path, exist_ok=True)

    def _get_path(self, player_id: PlayerId) -> str:
        """Return the file path for a given player ID."""
        return os.path.join(self._base_path, f"{player_id}.json")

    def save(self, player: Player) -> None:
        """Save a Player aggregate to a JSON file."""
        with open(self._get_path(PlayerId(player.id)), "w") as f:
            json.dump(player.to_dict(), f, indent=4)

    def get(self, player_id: PlayerId) -> Player | None:
        """Retrieve a Player aggregate from a JSON file, or None if not found."""
        filepath = self._get_path(player_id)
        if not os.path.exists(filepath):
            return None

        with open(filepath) as f:
            data: dict[str, Any] = json.load(f)

        return Player.from_dict(data)

    def get_by_name(self, name: str) -> Player | None:
        """Retrieve a Player aggregate by name, or None if not found."""
        if not os.path.exists(self._base_path):
            return None

        for filename in os.listdir(self._base_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self._base_path, filename)
                with open(filepath) as f:
                    data: dict[str, Any] = json.load(f)
                player = Player.from_dict(data)
                if player.name == name:
                    return player
        return None
