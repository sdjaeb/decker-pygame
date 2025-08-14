"""This module defines the application service for DSFile-related operations."""

from typing import Optional

from decker_pygame.application.dtos import DSFileDTO
from decker_pygame.domain.ids import DSFileId
from decker_pygame.ports.repository_interfaces import DSFileRepositoryInterface
from decker_pygame.ports.service_interfaces import DSFileServiceInterface


class DSFileService(DSFileServiceInterface):
    """Application service for DSFile-related operations."""

    def __init__(self, ds_file_repo: DSFileRepositoryInterface) -> None:
        self.ds_file_repo = ds_file_repo

    def get_ds_file_data(self, ds_file_id: DSFileId) -> Optional[DSFileDTO]:
        """Retrieves a DTO with data for a specific DSFile."""
        ds_file = self.ds_file_repo.get(ds_file_id)
        if not ds_file:
            return None

        return DSFileDTO.from_domain(ds_file)
