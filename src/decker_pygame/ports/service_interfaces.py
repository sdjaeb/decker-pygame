"""This module defines the interfaces for all application services.

In a Hexagonal Architecture, these interfaces act as the "driving ports" for the
application core. They define the set of use cases that the presentation layer
or any other external client can trigger.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.application.character_service import (
        CharacterDataDTO,
        CharacterViewData,
    )
    from decker_pygame.application.contract_service import ContractSummaryDTO
    from decker_pygame.application.deck_service import (
        DeckViewData,
        TransferViewData,
    )
    from decker_pygame.application.player_service import PlayerStatusDTO
    from decker_pygame.domain.crafting import Schematic
    from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId


class CharacterServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for character-related use cases."""

    @abstractmethod
    def get_character_data(
        self, character_id: "CharacterId"
    ) -> "CharacterDataDTO | None":
        """Retrieves raw data for a character."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def increase_skill(self, character_id: "CharacterId", skill_name: str) -> None:
        """Increases a character's skill level."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def decrease_skill(self, character_id: "CharacterId", skill_name: str) -> None:
        """Decreases a character's skill level."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_character_view_data(
        self, character_id: "CharacterId", player_id: "PlayerId"
    ) -> "CharacterViewData | None":
        """Retrieves a DTO with all data needed for the character view."""
        raise NotImplementedError  # pragma: no cover


class ContractServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for contract-related use cases."""

    @abstractmethod
    def get_available_contracts(self) -> list["ContractSummaryDTO"]:
        """Retrieves a list of currently available contracts."""
        raise NotImplementedError  # pragma: no cover


class CraftingServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for crafting-related use cases."""

    @abstractmethod
    def get_character_schematics(
        self, character_id: "CharacterId"
    ) -> list["Schematic"]:
        """Retrieves the list of schematics a character knows."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def craft_item(self, character_id: "CharacterId", schematic_name: str) -> None:
        """Orchestrates the use case of a character crafting an item."""
        raise NotImplementedError  # pragma: no cover


class DeckServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for deck-related use cases."""

    @abstractmethod
    def create_deck(self) -> "DeckId":
        """Creates a new, empty deck and returns its ID."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_deck_view_data(self, deck_id: "DeckId") -> "DeckViewData | None":
        """Retrieves and aggregates all data needed for the deck view."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def move_program_up(self, deck_id: "DeckId", program_name: str) -> None:
        """Moves a program up in the deck order."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def move_program_down(self, deck_id: "DeckId", program_name: str) -> None:
        """Moves a program down in the deck order."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_transfer_view_data(
        self, character_id: "CharacterId"
    ) -> "TransferViewData | None":
        """Retrieves and aggregates all data needed for the transfer view."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def move_program_to_deck(
        self, character_id: "CharacterId", program_name: str
    ) -> None:
        """Moves a program from a character's storage to their deck."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def move_program_to_storage(
        self, character_id: "CharacterId", program_name: str
    ) -> None:
        """Moves a program from a character's deck to their storage."""
        raise NotImplementedError  # pragma: no cover


class PlayerServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for player-related use cases."""

    @abstractmethod
    def get_player_status(self, player_id: "PlayerId") -> "PlayerStatusDTO | None":
        """Retrieves the current status of a player for UI display."""
        raise NotImplementedError  # pragma: no cover


class LoggingServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for logging operations."""

    @abstractmethod
    def log(self, message: str, data: dict[str, Any]) -> None:
        """Logs a message with associated structured data."""
        raise NotImplementedError  # pragma: no cover
