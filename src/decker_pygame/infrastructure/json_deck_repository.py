import json
import os
from typing import Any

from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import DeckId
from decker_pygame.ports.repository_interfaces import DeckRepositoryInterface


class JsonFileDeckRepository(DeckRepositoryInterface):
    """A concrete repository that persists Deck aggregates to JSON files."""

    def __init__(self, base_path: str) -> None:
        """Initialize the repository with a base directory for storage."""
        self._base_path = base_path
        os.makedirs(self._base_path, exist_ok=True)

    def _get_path(self, deck_id: DeckId) -> str:
        """Return the file path for a given deck ID."""
        return os.path.join(self._base_path, f"{deck_id}.json")

    def save(self, deck: Deck) -> None:
        """Save a Deck aggregate to a JSON file."""
        with open(self._get_path(DeckId(deck.id)), "w") as f:
            json.dump(deck.to_dict(), f, indent=4)

    def get(self, deck_id: DeckId) -> Deck | None:
        """Retrieve a Deck aggregate from a JSON file, or None if not found."""
        filepath = self._get_path(deck_id)
        if not os.path.exists(filepath):
            return None

        with open(filepath) as f:
            data: dict[str, Any] = json.load(f)

        return Deck.from_dict(data)
