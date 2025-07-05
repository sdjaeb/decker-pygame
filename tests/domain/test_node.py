import uuid

from decker_pygame.domain.ids import NodeId
from decker_pygame.domain.node import Node


def test_node_serialization_roundtrip():
    """Tests that a Node entity can be serialized and deserialized correctly."""
    node_id = NodeId(uuid.uuid4())
    original_node = Node(id=node_id, name="Mainframe")

    node_dict = original_node.to_dict()

    assert node_dict == {"id": str(node_id), "name": "Mainframe"}

    reconstituted_node = Node.from_dict(node_dict)

    assert reconstituted_node == original_node
    assert reconstituted_node.name == original_node.name
