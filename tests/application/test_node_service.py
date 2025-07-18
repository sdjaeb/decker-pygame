"""Tests for the NodeService."""

import pytest

from decker_pygame.application.dtos import FileAccessViewDTO
from decker_pygame.application.node_service import NodeService


@pytest.fixture
def node_service() -> NodeService:
    """Provides a NodeService instance for testing."""
    return NodeService()


def test_get_node_files_success(node_service: NodeService):
    """Tests retrieving files for a known node."""
    node_id = "corp_server_1"
    result = node_service.get_node_files(node_id)

    assert result is not None
    assert isinstance(result, FileAccessViewDTO)
    assert result.node_name == "Ares Corp Mainframe"
    assert len(result.files) == 4


def test_get_node_files_not_found(node_service: NodeService):
    """Tests retrieving files for an unknown node returns None."""
    result = node_service.get_node_files("unknown_node")
    assert result is None


@pytest.mark.parametrize(
    "node_id, password, expected",
    [
        ("corp_server_1", "blueice", True),
        ("corp_server_1", "wrongpassword", False),
        ("unknown_node", "anypassword", False),
    ],
)
def test_validate_password(node_service: NodeService, node_id, password, expected):
    """Tests password validation for various scenarios."""
    result = node_service.validate_password(node_id, password)
    assert result is expected
