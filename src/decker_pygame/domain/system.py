"""This module defines the System aggregate root."""

import uuid
from typing import Any

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, NodeId, SystemId


class System(AggregateRoot):
    """Represents a computer system that contains various nodes.

    Args:
        id (SystemId): Unique identifier for the system.
        name (str): Name of the system.
        node_ids (list[NodeId]): List of node IDs in the system.
    """

    def __init__(self, id: SystemId, name: str, node_ids: list[NodeId]) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.node_ids = node_ids

    def to_dict(self) -> dict[str, Any]:
        """Serialize the aggregate to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the System.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "node_ids": [str(nid) for nid in self.node_ids],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "System":
        """Reconstitute a System from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary data.

        Returns:
            "System": A System instance.
        """
        return cls(
            id=SystemId(uuid.UUID(data["id"])),
            name=data["name"],
            node_ids=[NodeId(uuid.UUID(nid)) for nid in data["node_ids"]],
        )
