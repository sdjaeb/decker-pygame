"""This module defines the interfaces for all repositories.

In a Hexagonal Architecture, these interfaces act as the "driven ports" for the
application core. They define the contract that infrastructure-layer persistence
components must adhere to.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, TypeVar

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import (
    CharacterId,
    ContractId,
    DeckId,
    DSFileId,
    PlayerId,
    SystemId,
)

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.domain.character import Character  # noqa: F401
    from decker_pygame.domain.contract import Contract
    from decker_pygame.domain.deck import Deck  # noqa: F401
    from decker_pygame.domain.ds_file import DSFile  # noqa: F401
    from decker_pygame.domain.player import Player
    from decker_pygame.domain.system import System  # noqa: F401

T = TypeVar("T", bound="AggregateRoot")
K = TypeVar("K")


class Repository[K, T](ABC):
    """A generic repository interface defining common persistence operations."""

    @abstractmethod
    def save(self, aggregate: T) -> None:
        """Saves an aggregate instance."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, id: K) -> Optional[T]:
        """Retrieves an aggregate instance by its ID."""
        raise NotImplementedError  # pragma: no cover


class CharacterRepositoryInterface(
    Repository[CharacterId, "Character"], ABC
):  # pragma: no cover
    """Interface for a repository that manages Character aggregates."""


class ContractRepositoryInterface(
    Repository[ContractId, "Contract"], ABC
):  # pragma: no cover
    """Interface for a repository that manages Contract aggregates."""

    @abstractmethod
    def get_all(self) -> list["Contract"]:
        """Retrieves all contracts."""
        raise NotImplementedError  # pragma: no cover


class DeckRepositoryInterface(Repository[DeckId, "Deck"], ABC):  # pragma: no cover
    """Interface for a repository that manages Deck aggregates."""


class DSFileRepositoryInterface(
    Repository[DSFileId, "DSFile"], ABC
):  # pragma: no cover
    """Interface for a repository that manages DSFile aggregates."""


class PlayerRepositoryInterface(
    Repository[PlayerId, "Player"], ABC
):  # pragma: no cover
    """Interface for a repository that manages Player aggregates."""

    @abstractmethod
    def get_by_name(self, name: str) -> Optional["Player"]:
        """Retrieves a player by their name."""
        raise NotImplementedError  # pragma: no cover


class SystemRepositoryInterface(
    Repository[SystemId, "System"], ABC
):  # pragma: no cover
    """Interface for a repository that manages System aggregates."""
