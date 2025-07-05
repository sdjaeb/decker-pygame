from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequiredResource:
    """
    A Value Object representing a resource needed for crafting.
    """

    name: str
    quantity: int


@dataclass(frozen=True)
class Schematic:
    """
    A Value Object representing the recipe to build an item.
    """

    name: str
    produces_item_name: str
    cost: list[RequiredResource]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the value object to a dictionary."""
        return {
            "name": self.name,
            "produces_item_name": self.produces_item_name,
            "cost": [c.__dict__ for c in self.cost],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Schematic":
        """Reconstitute a Schematic from a dictionary."""
        return cls(
            name=data["name"],
            produces_item_name=data["produces_item_name"],
            cost=[RequiredResource(**c_data) for c_data in data["cost"]],
        )
