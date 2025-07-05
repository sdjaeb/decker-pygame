import uuid
from typing import Any

from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import NodeId


class Node(Entity):
    """Represents a single node within a System."""

    def __init__(self, id: NodeId, name: str) -> None:
        """
        Initialize a Node.

        Args:
            id (NodeId): Unique identifier for the node.
            name (str): Name of the node.
        """
        super().__init__(id=id)
        self.name = name

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the entity to a dictionary.

        Returns:
            A dictionary representation of the Node.
        """
        return {"id": str(self.id), "name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        """
        Reconstitute a Node from a dictionary.

        Args:
            data: The dictionary data.

        Returns:
            A Node instance.
        """
        return cls(id=NodeId(uuid.UUID(data["id"])), name=data["name"])
