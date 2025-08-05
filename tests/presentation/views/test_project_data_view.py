"""This module contains tests for the ProjectDataView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import ProjectDataViewDTO, SourceCodeDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.label import Label
from decker_pygame.presentation.components.list_view import ListView
from decker_pygame.presentation.components.project_data_view import ProjectDataView


@pytest.fixture(autouse=True)
def pygame_init_fixture():
    """Fixture to initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_callbacks():
    """Provides a dictionary of mock callbacks."""
    return {
        "on_close": Mock(),
        "on_new_project": Mock(),
        "on_work_day": Mock(),
        "on_work_week": Mock(),
        "on_finish_project": Mock(),
        "on_build": Mock(),
        "on_trash": Mock(),
    }


@pytest.fixture
def sample_dto():
    """Provides a sample ProjectDataViewDTO for testing."""
    return ProjectDataViewDTO(
        date="Jan 1, 2072",
        project_type="Sentry ICE - 5",
        project_time_left="10 days",
        chip_type="None",
        chip_time_left="",
        source_codes=[
            SourceCodeDTO(
                id="1", type="Software", name="IcePick", rating=1, current_rating="-"
            ),
            SourceCodeDTO(
                id="2", type="Chip", name="Cortex Bomb", rating=2, current_rating="1"
            ),
        ],
        can_start_new_project=False,
        can_work_on_project=True,
    )


def test_initialization_and_widget_creation(sample_dto, mock_callbacks):
    """Tests that the view initializes correctly and creates its child widgets."""
    with (
        patch(
            "decker_pygame.presentation.components.project_data_view.Label", spec=Label
        ) as MockLabel,
        patch(
            "decker_pygame.presentation.components.project_data_view.ListView",
            spec=ListView,
        ) as MockListView,
        patch(
            "decker_pygame.presentation.components.project_data_view.Button",
            spec=Button,
        ) as MockButton,
    ):
        # Configure the mock instances to behave like sprites so they can be drawn
        for mock_class in [MockLabel, MockListView, MockButton]:
            mock_instance = mock_class.return_value
            mock_instance.image = pygame.Surface((10, 10))
            mock_instance.rect = mock_instance.image.get_rect()
            # Also mock set_enabled for Button
            if mock_class is MockButton:
                mock_instance.set_enabled = Mock()

        ProjectDataView(data=sample_dto, **mock_callbacks)

        # Assert labels were created
        assert MockLabel.call_count == 5

        # Assert ListView was created and populated
        MockListView.assert_called_once()
        mock_list_view_instance = MockListView.return_value
        mock_list_view_instance.set_items.assert_called_once()

        # Assert buttons were created
        assert MockButton.call_count == 7


def test_list_selection_enables_buttons(sample_dto, mock_callbacks):
    """Tests that selecting an item in the list enables the Build and Trash buttons."""
    view = ProjectDataView(data=sample_dto, **mock_callbacks)

    # Mock the buttons after they've been created
    view._build_button = Mock(spec=Button)
    view._trash_button = Mock(spec=Button)

    selected_item = sample_dto.source_codes[0]

    # Simulate the ListView calling our handler
    view._handle_selection_change(selected_item)

    assert view._selected_source_code is selected_item
    view._build_button.set_enabled.assert_called_once_with(True)
    view._trash_button.set_enabled.assert_called_once_with(True)


def test_list_deselection_disables_buttons(sample_dto, mock_callbacks):
    """Tests that deselecting an item disables the Build and Trash buttons."""
    view = ProjectDataView(data=sample_dto, **mock_callbacks)

    # Mock the buttons
    view._build_button = Mock(spec=Button)
    view._trash_button = Mock(spec=Button)

    # First select an item
    view._handle_selection_change(sample_dto.source_codes[0])
    view._build_button.set_enabled.assert_called_with(True)
    view._trash_button.set_enabled.assert_called_with(True)

    # Now deselect
    view._handle_selection_change(None)

    assert view._selected_source_code is None
    view._build_button.set_enabled.assert_called_with(False)
    view._trash_button.set_enabled.assert_called_with(False)


def test_handle_event_delegates_to_components(sample_dto, mock_callbacks):
    """Tests that the view correctly delegates events to its child components."""
    view = ProjectDataView(data=sample_dto, **mock_callbacks)

    # Replace a real component with a mock to check its handle_event
    mock_component = Mock(spec=Button)
    mock_component.handle_event = Mock()
    view._components.add(mock_component)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)})
    view.handle_event(event)

    mock_component.handle_event.assert_called_once()
    # Check that the event was translated to local coordinates
    called_event = mock_component.handle_event.call_args[0][0]
    assert called_event.pos != event.pos
    assert called_event.pos == (100 - view.rect.x, 100 - view.rect.y)
