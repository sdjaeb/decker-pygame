from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import NodeId


class Node(Entity):
    """Represents a single node within a System."""

    def __init__(self, id: NodeId, name: str) -> None:
        super().__init__(id=id)
        self.name = name
        # TODO: Add other Node attributes (e.g., type, security, etc.)
