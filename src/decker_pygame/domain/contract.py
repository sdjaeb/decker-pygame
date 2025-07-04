import uuid
from typing import Any

from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import AreaId, ContractId


class Contract(Entity):
    """Represents a job or mission a character can undertake."""

    def __init__(
        self,
        id: ContractId,
        title: str,
        client: str,
        target_area_id: AreaId,
        description: str,
        reward_credits: int,
    ) -> None:
        """
        Initialize a Contract.

        Args:
            id (ContractId): Unique identifier for the contract.
            title (str): Title of the contract.
            client (str): Client offering the contract.
            target_area_id (AreaId): Target area for the contract.
            description (str): Description of the contract.
            reward_credits (int): Reward for completing the contract.
        """
        super().__init__(id=id)
        self.title = title
        self.client = client
        self.target_area_id = target_area_id
        self.description = description
        self.reward_credits = reward_credits

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the entity to a dictionary.

        Returns:
            A dictionary representation of the Contract.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "client": self.client,
            "target_area_id": str(self.target_area_id),
            "description": self.description,
            "reward_credits": self.reward_credits,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contract":
        """
        Reconstitute a Contract from a dictionary.

        Args:
            data: The dictionary data.

        Returns:
            A Contract instance.
        """
        return cls(
            id=ContractId(uuid.UUID(data["id"])),
            title=data["title"],
            client=data["client"],
            target_area_id=AreaId(uuid.UUID(data["target_area_id"])),
            description=data["description"],
            reward_credits=data["reward_credits"],
        )
