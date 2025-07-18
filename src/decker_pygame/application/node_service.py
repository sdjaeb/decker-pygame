"""This module defines the application service for node-related operations."""

from typing import Optional

from decker_pygame.application.dtos import FileAccessViewDTO, FileDTO
from decker_pygame.ports.service_interfaces import NodeServiceInterface

# For now, we'll use a hardcoded map of nodes and their files. In the future,
# this would come from a Node aggregate and repository.
DUMMY_NODE_FILES = {
    "corp_server_1": FileAccessViewDTO(
        node_name="Ares Corp Mainframe",
        files=[
            FileDTO(name="access_codes.dat", size=128, file_type="Data"),
            FileDTO(name="employee_records.db", size=2048, file_type="Data"),
            FileDTO(name="jan_payroll.xls", size=512, file_type="Data"),
            FileDTO(name="sentry_ice_v2.prg", size=1024, file_type="Program"),
        ],
    )
}

# For now, we'll use a hardcoded map of nodes and their passwords.
DUMMY_NODE_PASSWORDS = {
    "corp_server_1": "blueice",
}


class NodeService(NodeServiceInterface):
    """Application service for node-related operations."""

    def get_node_files(self, node_id: str) -> Optional[FileAccessViewDTO]:
        """Retrieves a DTO with all data needed for the file access view.

        For now, this returns hardcoded data for a dummy node.
        """
        return DUMMY_NODE_FILES.get(node_id)

    def validate_password(self, node_id: str, password: str) -> bool:
        """Validates a password for a given node.

        For now, this checks against a hardcoded password.
        """
        correct_password = DUMMY_NODE_PASSWORDS.get(node_id)
        return correct_password is not None and correct_password == password
