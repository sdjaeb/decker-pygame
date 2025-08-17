"""Tests for the MatrixRunView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import MatrixRunViewDTO
from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.components.matrix_run_view import MatrixRunView


@pytest.fixture(autouse=True)
def pygame_init_fixture():
    """Fixture to initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture(autouse=True)
def reset_matrix_run_view_background():
    """Ensures the MatrixRunView._background is reset for each test."""
    original_background = MatrixRunView._background
    MatrixRunView._background = None
    yield
    MatrixRunView._background = original_background


@pytest.fixture
def mock_asset_service() -> Mock:
    """Provides a mock AssetService."""
    service = Mock(spec=AssetService)
    # Configure it to return real surfaces, as they are passed to pygame functions
    # that expect them.
    service.get_spritesheet.return_value = [pygame.Surface((16, 16))]
    service.get_image.return_value = pygame.Surface((1024, 768))
    return service


def test_matrix_run_view_initialization(mock_asset_service: Mock):
    """Tests that the view initializes its HUD components."""
    view = MatrixRunView(asset_service=mock_asset_service)
    # Check that the child views were created and added
    assert view.node_grid_view is not None
    assert view.map_view is not None
    assert view.message_view is not None
    assert view.software_list_view is not None
    assert view.alarm_bar is not None
    assert view.deck_health_bar is not None
    assert view.mental_health_bar is not None
    assert view.physical_health_bar is not None
    assert view.shield_status_bar is not None
    assert view.transfer_progress_bar is not None
    assert view.trace_progress_bar is not None
    assert view.ice_health_bar is not None
    assert view.clock_view is not None
    assert len(view.components) == 13
    mock_asset_service.get_image.assert_called_once_with("matrix_main")


def test_matrix_run_view_update(mock_asset_service: Mock):
    """Tests that the update method calls update on its children."""
    view = MatrixRunView(asset_service=mock_asset_service)

    # Create a mock DTO with some test data
    test_data = MatrixRunViewDTO(
        run_time_in_seconds=123,
        alarm_level=50.0,
        physical_health=75.0,
        mental_health=80.0,
        deck_health=90.0,
        shield_status=25.0,
        transfer_progress=10.0,
        trace_progress=5.0,
        ice_health=60.0,
        software=["TestProgram1", "TestProgram2"],
    )

    # Spy on the child components' update methods
    with (
        patch.object(view.clock_view, "update_time") as mock_clock_update,
        patch.object(view.alarm_bar, "set_percentage") as mock_alarm_update,
        patch.object(view.physical_health_bar, "set_percentage") as mock_phys_update,
        patch.object(view.mental_health_bar, "set_percentage") as mock_ment_update,
        patch.object(view.deck_health_bar, "set_percentage") as mock_deck_update,
        patch.object(view.shield_status_bar, "set_percentage") as mock_shield_update,
        patch.object(view.transfer_progress_bar, "set_percentage") as mock_trans_update,
        patch.object(view.trace_progress_bar, "set_percentage") as mock_trace_update,
        patch.object(view.ice_health_bar, "set_percentage") as mock_ice_update,
        patch.object(view.software_list_view, "set_software") as mock_software_update,
        patch.object(view.components, "update") as mock_group_update,
        patch.object(view.components, "draw") as mock_draw,
    ):
        view.update(test_data)

        # Assert that each component was updated with the correct data from the DTO
        mock_clock_update.assert_called_once_with(123)
        mock_alarm_update.assert_called_once_with(50.0)
        mock_phys_update.assert_called_once_with(75.0)
        mock_ment_update.assert_called_once_with(80.0)
        mock_deck_update.assert_called_once_with(90.0)
        mock_shield_update.assert_called_once_with(25.0)
        mock_trans_update.assert_called_once_with(10.0)
        mock_trace_update.assert_called_once_with(5.0)
        mock_ice_update.assert_called_once_with(60.0)
        mock_software_update.assert_called_once_with(["TestProgram1", "TestProgram2"])

        # Assert that the main sprite group methods were called
        mock_group_update.assert_called_once()
        mock_draw.assert_called_once()


def test_matrix_run_view_raises_error_if_background_missing(mock_asset_service: Mock):
    """Tests that MatrixRunView raises a ValueError if background is not found."""
    # Configure the mock to simulate the image being missing
    mock_asset_service.get_image.return_value = None

    with pytest.raises(
        ValueError, match="MatrixRunView background 'matrix_main' not found in assets."
    ):
        MatrixRunView(asset_service=mock_asset_service)
