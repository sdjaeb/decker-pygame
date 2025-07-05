import uuid
from typing import Any

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, AreaId, ContractId


class Area(AggregateRoot):
    """Represents a location or region in the game world."""

    def __init__(
        self,
        id: AreaId,
        name: str,
        description: str,
        security_level: int,
        contract_ids: list[ContractId],
    ) -> None:
        """
        Initialize an Area.

        Args:
            id (AreaId): Unique identifier for the area.
            name (str): Name of the area.
            description (str): Description of the area.
            security_level (int): Security level of the area.
            contract_ids (List[ContractId]): Contracts available in the area.
        """
        super().__init__(id=AggregateId(id))
        self.name = name
        self.description = description
        self.security_level = security_level
        self.contract_ids = contract_ids

    def add_contract(self, contract_id: ContractId) -> None:
        """
        Add a contract to the area.

        Args:
            contract_id (ContractId): The contract to add.

        Returns:
            None
        """
        self.contract_ids.append(contract_id)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the aggregate to a dictionary.

        Returns:
            A dictionary representation of the Area.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "security_level": self.security_level,
            "contract_ids": [str(cid) for cid in self.contract_ids],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Area":
        """
        Reconstitute an Area from a dictionary.

        Args:
            data: The dictionary data.

        Returns:
            An Area instance.
        """
        return cls(
            id=AreaId(uuid.UUID(data["id"])),
            name=data["name"],
            description=data["description"],
            security_level=data["security_level"],
            contract_ids=[ContractId(uuid.UUID(cid)) for cid in data["contract_ids"]],
        )
