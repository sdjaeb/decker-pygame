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
