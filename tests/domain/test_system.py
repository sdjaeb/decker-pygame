import uuid

from decker_pygame.domain.ids import NodeId, SystemId
from decker_pygame.domain.system import System


def test_system_serialization_roundtrip():
    """Tests that a System can be serialized and deserialized correctly."""
    system_id = SystemId(uuid.uuid4())
    node_id = NodeId(uuid.uuid4())
    original_system = System(id=system_id, name="Ares Corporate HQ", node_ids=[node_id])

    system_dict = original_system.to_dict()

    assert system_dict == {
        "id": str(system_id),
        "name": "Ares Corporate HQ",
        "node_ids": [str(node_id)],
    }

    reconstituted_system = System.from_dict(system_dict)

    assert reconstituted_system == original_system
    assert reconstituted_system.name == original_system.name
    assert reconstituted_system.node_ids == original_system.node_ids
