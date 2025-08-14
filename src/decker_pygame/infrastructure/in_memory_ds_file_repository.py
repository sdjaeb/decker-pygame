"""An in-memory implementation of the DSFile repository interface."""

from typing import Optional

from decker_pygame.domain.ds_file import DSFile
from decker_pygame.domain.ids import DSFileId
from decker_pygame.ports.repository_interfaces import DSFileRepositoryInterface


class InMemoryDSFileRepository(DSFileRepositoryInterface):
    """A concrete repository that stores DSFile aggregates in memory.

    This is useful for testing purposes.
    """

    def __init__(self) -> None:
        self._ds_files: dict[DSFileId, DSFile] = {}

    def save(self, ds_file: DSFile) -> None:
        """Save a DSFile aggregate to the in-memory store."""
        self._ds_files[ds_file.id] = ds_file

    def get(self, ds_file_id: DSFileId) -> Optional[DSFile]:
        """Retrieve a DSFile aggregate from the in-memory store."""
        return self._ds_files.get(ds_file_id)
