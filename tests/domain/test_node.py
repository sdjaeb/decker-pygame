import uuid

from decker_pygame.domain.ids import NodeId
from decker_pygame.domain.node import Node


def test_node_creation():
    """Tests creating a node."""
    node_id = NodeId(uuid.uuid4())
    node = Node(id=node_id, name="CPU")

    assert node.id == node_id
    assert node.name == "CPU"
