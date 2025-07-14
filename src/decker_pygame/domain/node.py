"""This module defines the Node entity."""

import uuid
from typing import Any

from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import NodeId


class Node(Entity):
    """Represents a single node within a System.

    Args:
        id (NodeId): Unique identifier for the node.
        name (str): Name of the node.
    """

    def __init__(self, id: NodeId, name: str) -> None:
        super().__init__(id=id)
        self.name = name

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entity to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the Node.
        """
        return {"id": str(self.id), "name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        """Reconstitute a Node from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary data.

        Returns:
            "Node": A Node instance.
        """
        return cls(id=NodeId(uuid.UUID(data["id"])), name=data["name"])
