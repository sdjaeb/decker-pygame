from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.application.character_service import (
        CharacterDataDTO,
        CharacterViewData,
    )
    from decker_pygame.application.contract_service import ContractSummaryDTO
    from decker_pygame.application.deck_service import DeckViewData
    from decker_pygame.application.player_service import PlayerStatusDTO
    from decker_pygame.domain.crafting import Schematic
    from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId


class CharacterServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for character-related use cases."""

    @abstractmethod
    def get_character_data(
        self, character_id: "CharacterId"
    ) -> "CharacterDataDTO | None":
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def increase_skill(self, character_id: "CharacterId", skill_name: str) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def decrease_skill(self, character_id: "CharacterId", skill_name: str) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_character_view_data(
        self, character_id: "CharacterId", player_id: "PlayerId"
    ) -> "CharacterViewData | None":
        raise NotImplementedError  # pragma: no cover


class ContractServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for contract-related use cases."""

    @abstractmethod
    def get_available_contracts(self) -> list["ContractSummaryDTO"]:
        raise NotImplementedError  # pragma: no cover


class CraftingServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for crafting-related use cases."""

    @abstractmethod
    def get_character_schematics(
        self, character_id: "CharacterId"
    ) -> list["Schematic"]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def craft_item(self, character_id: "CharacterId", schematic_name: str) -> None:
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


class PlayerServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for player-related use cases."""

    @abstractmethod
    def get_player_status(self, player_id: "PlayerId") -> "PlayerStatusDTO | None":
        raise NotImplementedError  # pragma: no cover


class LoggingServiceInterface(ABC):  # pragma: no cover
    """Defines the input port for logging operations."""

    @abstractmethod
    def log(self, message: str, data: dict[str, Any]) -> None:
        raise NotImplementedError  # pragma: no cover
