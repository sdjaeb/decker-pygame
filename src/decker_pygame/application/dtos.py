"""This module defines Data Transfer Objects (DTOs) for the application layer."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict

from decker_pygame.domain.ids import ContractId, DeckId
from decker_pygame.domain.shop import ShopItemType

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.domain.contract import Contract


@dataclass
class MissionResultsDTO:
    """Data for displaying the results of a mission.

    Attributes:
        contract_name (str): The name of the completed contract.
        was_successful (bool): Whether the mission was successful.
        credits_earned (int): The amount of credits earned from the mission.
        reputation_change (int): The change in the player's reputation
            resulting from the mission.
    """

    contract_name: str
    was_successful: bool
    credits_earned: int
    reputation_change: int


@dataclass
class RestViewDTO:
    """Data for displaying the rest view.

    Attributes:
        cost (int): The cost of resting, in credits.
        health_recovered (int): The amount of health the player recovers
            after resting.
    """

    cost: int
    health_recovered: int


@dataclass
class PlayerStatusDTO:
    """Data for displaying the player's current status.

    Attributes:
        current_health (int): The player's current health points.
        max_health (int): The player's maximum health points.
    """

    current_health: int
    max_health: int


@dataclass
class CharacterDataDTO:
    """Data for a character's core attributes.

    Attributes:
        name (str): The character's name.
        credits (int): The amount of credits the character has.
        skills (dict[str, Any]): A dictionary of the character's skills
            and their levels.
        unused_skill_points (int): The number of skill points the character
            has available to spend.
        deck_id (DeckId): The ID of the character's associated deck.
    """

    name: str
    credits: int
    skills: dict[str, Any]
    unused_skill_points: int
    deck_id: DeckId


@dataclass
class CharacterViewDTO:
    """Data for displaying character information in a view.

    Attributes:
        name (str): The character's name.
        credits (int): The amount of credits the character has.
        reputation (int): The character's reputation level.
        skills (dict[str, Any]): A dictionary of the character's skills
            and their levels.
        unused_skill_points (int): The number of skill points the character
            has available to spend.
        health (int): The character's current health points.
    """

    name: str
    credits: int
    reputation: int
    skills: dict[str, Any]
    unused_skill_points: int
    health: int


@dataclass
class ProgramDTO:
    """Data for a single program.

    Attributes:
        name (str): The name of the program.
        size (int): The size of the program, likely representing its
            memory or storage requirements.
    """

    name: str
    size: int


@dataclass
class DeckViewDTO:
    """Data for displaying the contents of a deck.

    Attributes:
        programs (list[ProgramDTO]): A list of ProgramDTOs representing the
            programs in the deck.
        used_deck_size (int): The current number of slots used in the deck.
        total_deck_size (int): The maximum capacity of the deck.
    """

    programs: list[ProgramDTO]
    used_deck_size: int
    total_deck_size: int


@dataclass
class ShopItemDTO:
    """Data for a single item available in a shop.

    Attributes:
        name (str): The name of the item.
        cost (int): The cost of the item in credits.
        description (str): A brief description of the item, providing
            additional context or details about its functionality or
            purpose.
    """

    name: str
    cost: int
    description: str


@dataclass
class ShopViewDTO:
    """Data for displaying a shop's inventory.

    Attributes:
        shop_name (str): The name of the shop.
        items (list[ShopItemDTO]): A list of available shop items.
    """

    shop_name: str
    items: list[ShopItemDTO]


@dataclass
class ShopItemViewDTO:
    """Data Transfer Object for displaying detailed shop item information.

    Attributes:
        name (str): The name of the item.
        cost (int): The cost of the item in credits.
        description (str): A description of the item.
        item_type (ShopItemType): The type of the item.
        other_stats (dict[str, int]): A dictionary of other relevant stats.
    """

    name: str
    cost: int
    description: str
    item_type: ShopItemType
    other_stats: dict[str, int]


@dataclass
class IceDataViewDTO:
    """Data for displaying detailed information about an ICE program.

    Attributes:
        name (str): The name of the ICE program.
        ice_type (str): The type or category of the ICE program.
        strength (int): The strength or effectiveness of the ICE program.
        description (str): A description of the ICE program, providing
            details about its function or effects.
        cost (int): The cost of the ICE program, which might be relevant
            in contexts where the player could acquire or use it.
    """

    name: str
    ice_type: str
    strength: int
    description: str
    cost: int


@dataclass
class TransferViewDTO:
    """Data for displaying the transfer view.

    Attributes:
        deck_programs (list[ProgramDTO]): A list of ProgramDTOs representing
            programs currently in the deck.
        stored_programs (list[ProgramDTO]): A list of ProgramDTOs representing
            programs currently in storage.
    """

    deck_programs: list[ProgramDTO]
    stored_programs: list[ProgramDTO]


class FileDTO(TypedDict):
    """Data for a single file on a node.

    Attributes:
        name (str): The name of the file.
        size (int): The size of the file in KB or some other unit.
        file_type (str): The type of the file (e.g., "data", "program").
    """

    name: str
    size: int
    file_type: str


@dataclass
class FileAccessViewDTO:
    """Data for displaying the file access view for a node.

    Attributes:
        node_name (str): The name of the node being accessed.
        files (list[FileDTO]): A list of files on the node.
    """

    node_name: str
    files: list[FileDTO]


@dataclass(frozen=True)
class ContractSummaryDTO:
    """A summary of a contract for list views.

    Attributes:
        id (ContractId): The unique identifier of the contract.
        title (str): The title or name of the contract.
        client (str): The name or identifier of the contract's client.
        reward (int): The reward offered for completing the contract,
            typically in credits.
    """

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
