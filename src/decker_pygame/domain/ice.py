"""This module defines the Ice entity."""

import uuid
from typing import Any

from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import IceId


class Ice(Entity):
    """Represents Intrusion Countermeasures Electronics (ICE)."""

    def __init__(self, id: IceId, name: str, strength: int) -> None:
        """Initialize an Ice entity.

        Args:
            id (IceId): Unique identifier for the ICE.
            name (str): Name of the ICE.
            strength (int): Strength of the ICE.
        """
        super().__init__(id=id)
        self.name = name
        self.strength = strength

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entity to a dictionary.

        Returns:
            A dictionary representation of the Ice.
        """
        return {"id": str(self.id), "name": self.name, "strength": self.strength}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Ice":
        """Reconstitute an Ice from a dictionary.

        Args:
            data: The dictionary data.

        Returns:
            An Ice instance.
        """
        return cls(
            id=IceId(uuid.UUID(data["id"])),
            name=data["name"],
            strength=data["strength"],
        )
