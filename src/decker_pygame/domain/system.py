"""This module defines the System aggregate root."""

import uuid
from dataclasses import dataclass
from typing import Any

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, NodeId, SystemId


@dataclass(frozen=True)
class Node:
    """A value object representing a node within a system."""

    id: NodeId
    name: str
    position: tuple[int, int]  # (x, y) coordinates for map view

    def to_dict(self) -> dict[str, Any]:
        """Serialize the node to a dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        """Reconstitute a Node from a dictionary."""
        return cls(
            id=NodeId(uuid.UUID(data["id"])),
            name=data["name"],
            position=tuple(data["position"]),
        )


class System(AggregateRoot):
    """Represents a computer system that contains various nodes and their layout.

    Args:
        id (SystemId): Unique identifier for the system.
        name (str): Name of the system.
        nodes (list[Node]): List of nodes in the system.
        connections (list[tuple[NodeId, NodeId]]): List of connections between nodes.
    """

    def __init__(
        self,
        id: SystemId,
        name: str,
        nodes: list[Node],
        connections: list[tuple[NodeId, NodeId]],
    ) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.nodes = nodes
        self.connections = connections

    def __eq__(self, other: object) -> bool:
        """Compares this System with another object for equality."""
        if not isinstance(other, System):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.nodes == other.nodes
            and self.connections == other.connections
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the aggregate to a dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "nodes": [node.to_dict() for node in self.nodes],
            "connections": [[str(start), str(end)] for start, end in self.connections],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "System":
        """Reconstitute a System from a dictionary."""
        return cls(
            id=SystemId(uuid.UUID(data["id"])),
            name=data["name"],
            nodes=[Node.from_dict(n_data) for n_data in data["nodes"]],
            connections=[
                (NodeId(uuid.UUID(start)), NodeId(uuid.UUID(end)))
                for start, end in data["connections"]
            ],
        )
