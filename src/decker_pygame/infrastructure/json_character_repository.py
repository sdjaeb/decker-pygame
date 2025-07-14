"""A JSON file-based implementation of the Character repository interface."""

import json
import os

from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface


class JsonFileCharacterRepository(CharacterRepositoryInterface):
    """A concrete repository that persists Character aggregates to JSON files.

    Each character is stored in a separate file named after its ID.

    Args:
        base_path (str): Directory where character files are stored.
    """

    def __init__(self, base_path: str) -> None:
        self._base_path = base_path
        os.makedirs(self._base_path, exist_ok=True)

    def _get_path(self, character_id: CharacterId) -> str:
        """Return the file path for a given character ID."""
        return os.path.join(self._base_path, f"{character_id}.json")

    def save(self, character: Character) -> None:
        """Save a Character aggregate to a JSON file."""
        with open(self._get_path(CharacterId(character.id)), "w") as f:
            json.dump(character.to_dict(), f, indent=4)

    def get(self, character_id: CharacterId) -> Character | None:
        """Retrieve a Character aggregate from a JSON file, or None if not found."""
        filepath = self._get_path(character_id)
        if not os.path.exists(filepath):
            return None

        with open(filepath) as f:
            data = json.load(f)

        return Character.from_dict(data)
