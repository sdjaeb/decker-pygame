"""Tests for the MatrixRunView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

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
    assert len(view.components) == 12
    mock_asset_service.get_image.assert_called_once_with("matrix_main")


def test_matrix_run_view_update(mock_asset_service: Mock):
    """Tests that the update method calls update on its children."""
    view = MatrixRunView(asset_service=mock_asset_service)
    # Spy on the components group
    with patch.object(view.components, "update") as mock_update:
        with patch.object(view.components, "draw") as mock_draw:
            view.update()
            mock_update.assert_called_once()
            mock_draw.assert_called_once()


def test_matrix_run_view_raises_error_if_background_missing(mock_asset_service: Mock):
    """Tests that MatrixRunView raises a ValueError if background is not found."""
    # Configure the mock to simulate the image being missing
    mock_asset_service.get_image.return_value = None

    with pytest.raises(
        ValueError, match="MatrixRunView background 'matrix_main' not found in assets."
    ):
        MatrixRunView(asset_service=mock_asset_service)
