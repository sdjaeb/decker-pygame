"""This module defines Data Transfer Objects (DTOs) for the application layer."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from decker_pygame.domain.ids import ContractId, DeckId

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.domain.contract import Contract


@dataclass
class MissionResultsDTO:
    """Data for displaying the results of a mission."""

    contract_name: str
    was_successful: bool
    credits_earned: int
    reputation_change: int


@dataclass
class RestViewDTO:
    """Data for displaying the rest view."""

    cost: int
    health_recovered: int


@dataclass
class PlayerStatusDTO:
    """Data for displaying the player's current status."""

    current_health: int
    max_health: int


@dataclass
class CharacterDataDTO:
    """Data for a character's core attributes."""

    name: str
    credits: int
    skills: dict[str, Any]
    unused_skill_points: int
    deck_id: DeckId


@dataclass
class CharacterViewDTO:
    """Data for displaying character information in a view."""

    name: str
    credits: int
    reputation: int
    skills: dict[str, Any]
    unused_skill_points: int
    health: int


@dataclass
class ProgramDTO:
    """Data for a single program."""

    name: str
    size: int


@dataclass
class DeckViewDTO:
    """Data for displaying the contents of a deck."""

    programs: list[ProgramDTO]
    used_deck_size: int
    total_deck_size: int


@dataclass
class ShopItemDTO:
    """Data for a single item available in a shop."""

    name: str
    cost: int
    description: str


@dataclass
class ShopViewDTO:
    """Data for displaying a shop's inventory."""

    shop_name: str
    items: list[ShopItemDTO]


@dataclass
class IceDataViewDTO:
    """Data for displaying detailed information about an ICE program."""

    name: str
    ice_type: str
    strength: int
    description: str
    cost: int


@dataclass
class TransferViewDTO:
    """Data for displaying the transfer view."""

    deck_programs: list[ProgramDTO]
    stored_programs: list[ProgramDTO]


@dataclass(frozen=True)
class ContractSummaryDTO:
    """A summary of a contract for list views."""

    id: ContractId
    title: str
    client: str
    reward: int

    @classmethod
    def from_domain(cls, contract: "Contract") -> "ContractSummaryDTO":
        """Create a DTO from a Contract domain object."""
        return cls(
            id=ContractId(contract.id),
            title=contract.title,
            client=contract.client,
            reward=contract.reward_credits,
        )
