import uuid

from decker_pygame.domain.ids import SystemId
from decker_pygame.domain.system import System


def test_system_creation():
    """Tests creating a system."""
    system_id = SystemId(uuid.uuid4())
    system = System(id=system_id, name="Corporate Mainframe")

    assert system.id == system_id
    assert system.name == "Corporate Mainframe"
    assert system.node_ids == []
