from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from decker_pygame.domain.character import Character
    from decker_pygame.domain.contract import Contract
    from decker_pygame.domain.ids import CharacterId, ContractId, PlayerId
    from decker_pygame.domain.player import Player


class CharacterRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Character aggregates."""

    @abstractmethod
    def save(self, character: "Character") -> None:
        """Saves a character."""
        raise NotImplementedError

    @abstractmethod
    def get(self, character_id: "CharacterId") -> Optional["Character"]:
        """Retrieves a character by its ID."""
        raise NotImplementedError


class ContractRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Contract aggregates."""

    @abstractmethod
    def get_all(self) -> list["Contract"]:
        """Retrieves all contracts."""
        raise NotImplementedError

    @abstractmethod
    def save(self, contract: "Contract") -> None:
        """Saves a contract."""
        raise NotImplementedError

    @abstractmethod
    def get(self, contract_id: "ContractId") -> Optional["Contract"]:
        """Retrieves a contract by its ID."""
        raise NotImplementedError


class PlayerRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Player aggregates."""

    @abstractmethod
    def save(self, player: "Player") -> None:
        """Saves a player."""
        raise NotImplementedError

    @abstractmethod
    def get(self, player_id: "PlayerId") -> Optional["Player"]:
        """Retrieves a player by its ID."""
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Optional["Player"]:
        """Retrieves a player by their name."""
        raise NotImplementedError
