"""This module defines the interfaces for all data repositories.

In a Hexagonal Architecture, these interfaces act as the "driven ports" for the
application core. They define the contracts that persistence-layer adapters
must adhere to, allowing the application to remain ignorant of the specific
database or storage technology being used.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.domain.character import Character
    from decker_pygame.domain.contract import Contract
    from decker_pygame.domain.deck import Deck
    from decker_pygame.domain.ds_file import DSFile
    from decker_pygame.domain.ids import (
        CharacterId,
        ContractId,
        DeckId,
        DSFileId,
        PlayerId,
    )
    from decker_pygame.domain.player import Player


class CharacterRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Character aggregates."""

    @abstractmethod
    def save(self, character: "Character") -> None:
        """Saves a character."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, character_id: "CharacterId") -> Optional["Character"]:
        """Retrieves a character by its ID."""
        raise NotImplementedError  # pragma: no cover


class ContractRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Contract aggregates."""

    @abstractmethod
    def get_all(self) -> list["Contract"]:
        """Retrieves all contracts."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def save(self, contract: "Contract") -> None:
        """Saves a contract."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, contract_id: "ContractId") -> Optional["Contract"]:
        """Retrieves a contract by its ID."""
        raise NotImplementedError  # pragma: no cover


class DeckRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Deck aggregates."""

    @abstractmethod
    def save(self, deck: "Deck") -> None:
        """Saves a deck."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, deck_id: "DeckId") -> Optional["Deck"]:
        """Retrieves a deck by its ID."""
        raise NotImplementedError  # pragma: no cover


class DSFileRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages DSFile aggregates."""

    @abstractmethod
    def save(self, ds_file: "DSFile") -> None:
        """Saves a DSFile."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, ds_file_id: "DSFileId") -> Optional["DSFile"]:
        """Retrieves a DSFile by its ID."""
        raise NotImplementedError  # pragma: no cover


class PlayerRepositoryInterface(ABC):  # pragma: no cover
    """Interface for a repository that manages Player aggregates."""

    @abstractmethod
    def save(self, player: "Player") -> None:
        """Saves a player."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, player_id: "PlayerId") -> Optional["Player"]:
        """Retrieves a player by its ID."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_name(self, name: str) -> Optional["Player"]:
        """Retrieves a player by their name."""
        raise NotImplementedError  # pragma: no cover
