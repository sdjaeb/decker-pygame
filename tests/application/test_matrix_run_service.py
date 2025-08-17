"""Tests for the MatrixRunService."""

import uuid

from decker_pygame.application.dtos import MatrixRunViewDTO
from decker_pygame.application.matrix_run_service import MatrixRunService
from decker_pygame.domain.ids import CharacterId


def test_get_matrix_run_view_data() -> None:
    """Tests that the service returns the expected (currently hardcoded) DTO."""
    service = MatrixRunService()
    character_id = CharacterId(uuid.uuid4())

    dto = service.get_matrix_run_view_data(character_id)

    assert isinstance(dto, MatrixRunViewDTO)
    assert dto.alarm_level == 10.0
    assert dto.physical_health == 95.0
    assert "Hammer v1" in dto.software
