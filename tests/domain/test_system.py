import uuid

from decker_pygame.domain.ids import NodeId, SystemId
from decker_pygame.domain.system import Node, System


def test_system_serialization_roundtrip():
    """Tests that a System can be serialized and deserialized correctly."""
    system_id = SystemId(uuid.uuid4())
    node_id = NodeId(uuid.uuid4())
    node = Node(id=node_id, name="CPU", position=(50, 50))
    original_system = System(
        id=system_id,
        name="Ares Corporate HQ",
        nodes=[node],
        connections=[(node_id, node_id)],  # A self-referencing connection for test
    )

    system_dict = original_system.to_dict()

    assert system_dict == {
        "id": str(system_id),
        "name": "Ares Corporate HQ",
        "nodes": [{"id": str(node_id), "name": "CPU", "position": (50, 50)}],
        "connections": [[str(node_id), str(node_id)]],
    }

    reconstituted_system = System.from_dict(system_dict)

    assert reconstituted_system == original_system


def test_system_inequality_with_other_types():
    """Tests that a System is not equal to an object of a different type."""
    system = System(
        id=SystemId(uuid.uuid4()),
        name="Test System",
        nodes=[],
        connections=[],
    )
    # This comparison should exercise the 'return NotImplemented' path in __eq__
    assert system != "a string"
