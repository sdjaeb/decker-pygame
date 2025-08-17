"""This module defines the service for matrix run-related use cases."""

from decker_pygame.application.dtos import MatrixRunViewDTO
from decker_pygame.domain.ids import CharacterId
from decker_pygame.ports.service_interfaces import MatrixRunServiceInterface


class MatrixRunService(MatrixRunServiceInterface):
    """Service for handling matrix run logic."""

    def get_matrix_run_view_data(self, character_id: CharacterId) -> MatrixRunViewDTO:
        """Retrieves a DTO with all data needed for the matrix run view.

        For now, this returns hardcoded data.
        """
        # TODO: Replace with real data from domain aggregates
        return MatrixRunViewDTO(
            run_time_in_seconds=0,
            alarm_level=10.0,
            physical_health=95.0,
            mental_health=88.0,
            deck_health=100.0,
            shield_status=0.0,
            transfer_progress=0.0,
            trace_progress=0.0,
            ice_health=0.0,
            messages=["Welcome to the Matrix."],
            software=["Hammer v1", "IcePick v2"],
        )
