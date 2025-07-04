from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, NodeId, SystemId


class System(AggregateRoot):
    """Represents a computer system that contains various nodes."""

    def __init__(self, id: SystemId, name: str, node_ids: list[NodeId]) -> None:
        """
        Initialize a System.

        Args:
            id (SystemId): Unique identifier for the system.
            name (str): Name of the system.
            node_ids (list[NodeId]): List of node IDs in the system.
        """
        super().__init__(id=AggregateId(id))
        self.name = name
        self.node_ids = node_ids
