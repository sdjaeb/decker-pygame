"""This module defines domain objects related to crafting."""

from dataclasses import asdict, dataclass
from typing import Any
from uuid import UUID

from decker_pygame.domain.ids import SchematicId
from decker_pygame.domain.project import ProjectType


@dataclass(frozen=True)
class RequiredResource:
    """A Value Object representing a resource required for crafting."""

    name: str
    quantity: int


@dataclass(frozen=True)
class Schematic:
    """A Value Object representing a blueprint for crafting an item."""

    id: SchematicId
    type: ProjectType
    name: str
    produces_item_name: str
    produces_item_size: int
    rating: int
    cost: list[RequiredResource]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the value object to a dictionary."""
        data = asdict(self)
        data["id"] = str(self.id)
        data["type"] = self.type.value
        data["cost"] = [asdict(r) for r in self.cost]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Schematic":
        """Reconstitute a Schematic from a dictionary."""
        data_copy = data.copy()
        data_copy["id"] = SchematicId(UUID(data_copy["id"]))
        data_copy["type"] = ProjectType(data_copy["type"])
        data_copy["cost"] = [
            RequiredResource(**r_data) for r_data in data_copy.get("cost", [])
        ]
        return cls(**data_copy)
