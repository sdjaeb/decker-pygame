from abc import ABC, abstractmethod

from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId


class CharacterRepositoryInterface(ABC):
    """Abstract base class for character repository implementations."""

    @abstractmethod
    def get(self, character_id: CharacterId) -> Character | None:
        """Retrieve a character by ID.

        Args:
            character_id: The ID of the character.

        Returns:
            The character if found, else None.
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def save(self, character: Character) -> None:
        """Save a character aggregate."""
        raise NotImplementedError  # pragma: no cover
