import abc

from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId


class CharacterRepositoryInterface(abc.ABC):
    """Abstract base class for character repository implementations."""

    @abc.abstractmethod
    def get(self, character_id: CharacterId) -> Character | None:
        """Retrieve a character by ID.

        Args:
            character_id: The ID of the character.

        Returns:
            The character if found, else None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, character: Character) -> None:
        """Save a character aggregate."""
        raise NotImplementedError
