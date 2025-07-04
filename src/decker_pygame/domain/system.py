from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, NodeId, SystemId


class System(AggregateRoot):
    """Represents a computer system that contains various nodes."""

    def __init__(self, id: SystemId, name: str) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.node_ids: list[NodeId] = []
        # TODO: Add methods to manage nodes within the system
