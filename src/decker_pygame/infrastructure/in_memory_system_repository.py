"""This module provides an in-memory implementation of the SystemRepository."""

from typing import Optional

from decker_pygame.domain.ids import SystemId
from decker_pygame.domain.system import System
from decker_pygame.ports.repository_interfaces import SystemRepositoryInterface


class InMemorySystemRepository(SystemRepositoryInterface):
    """An in-memory repository for System aggregates."""

    def __init__(self) -> None:
        self._systems: dict[SystemId, System] = {}

    def save(self, system: System) -> None:
        """Save a System aggregate to the in-memory store."""
        self._systems[SystemId(system.id)] = system

    def get(self, system_id: SystemId) -> Optional[System]:
        """Retrieve a System aggregate from the in-memory store."""
        return self._systems.get(system_id)
