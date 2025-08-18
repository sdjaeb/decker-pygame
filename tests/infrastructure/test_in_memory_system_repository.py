"""This module contains tests for the InMemorySystemRepository."""

import uuid

from decker_pygame.domain.ids import NodeId, SystemId
from decker_pygame.domain.system import Node, System
from decker_pygame.infrastructure.in_memory_system_repository import (
    InMemorySystemRepository,
)


def test_save_and_get_system():
    """Tests that a System can be saved and retrieved."""
    # Arrange
    repo = InMemorySystemRepository()
    system_id = SystemId(uuid.uuid4())
    node_id = NodeId(uuid.uuid4())
    system = System(
        id=system_id,
        name="Test System",
        nodes=[Node(id=node_id, name="CPU", position=(10, 10))],
        connections=[],
    )

    # Act
    repo.save(system)
    retrieved_system = repo.get(system_id)

    # Assert
    assert retrieved_system is not None
    assert retrieved_system.id == system_id
    assert retrieved_system.name == "Test System"
    assert len(retrieved_system.nodes) == 1
    assert retrieved_system.nodes[0].name == "CPU"


def test_get_non_existent_system():
    """Tests that getting a non-existent System returns None."""
    repo = InMemorySystemRepository()
    non_existent_id = SystemId(uuid.uuid4())

    retrieved_system = repo.get(non_existent_id)

    assert retrieved_system is None
