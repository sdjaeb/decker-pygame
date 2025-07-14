"""This module defines the Ice entity."""

import uuid
from typing import Any

from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import IceId


class Ice(Entity):
    """Represents Intrusion Countermeasures Electronics (ICE)."""

    def __init__(self, id: IceId, name: str, strength: int) -> None:
        super().__init__(id=id)
        self.name = name
        self.strength = strength

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entity to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the Ice.
        """
        return {"id": str(self.id), "name": self.name, "strength": self.strength}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Ice":
        """Reconstitute an Ice from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary data.

        Returns:
            "Ice": An Ice instance.
        """
        return cls(
            id=IceId(uuid.UUID(data["id"])),
            name=data["name"],
            strength=data["strength"],
        )
