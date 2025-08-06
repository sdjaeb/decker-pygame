"""This module contains tests for the NewProjectView component."""

from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.application.dtos import NewProjectViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.new_project_view import NewProjectView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def new_project_data() -> NewProjectViewDTO:
    """Provides a sample NewProjectViewDTO for testing."""
    return NewProjectViewDTO(
        programming_skill=5,
        chip_design_skill=2,
        available_software=["Sentry ICE", "Hammer"],
        available_chips=["Cortex Bomb"],
    )


@pytest.fixture
def view(
    new_project_data: NewProjectViewDTO,
) -> tuple[NewProjectView, Mock, Mock]:
    """Provides a NewProjectView instance with mock callbacks."""
    on_start = Mock()
    on_close = Mock()
    view_instance = NewProjectView(
        data=new_project_data, on_start=on_start, on_close=on_close
    )
    return view_instance, on_start, on_close


def test_new_project_view_initialization(view: tuple[NewProjectView, Mock, Mock]):
    """Tests that the view initializes correctly and renders the default tab."""
    view_instance, _, _ = view

    # Check that it starts on the software tab
    assert view_instance._active_tab == "software"
    assert view_instance._data.programming_skill == 5


def test_tab_switching(view: tuple[NewProjectView, Mock, Mock]):
    """Tests that clicking the tabs changes the active view."""
    view_instance, _, _ = view

    # Simulate click on chip tab button
    chip_tab_button = view_instance._chip_tab_button
    click_pos = chip_tab_button.rect.center
    global_click_pos = (
        click_pos[0] + view_instance.rect.x,
        click_pos[1] + view_instance.rect.y,
    )
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": global_click_pos}
    )
    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": global_click_pos}
    )
    view_instance.handle_event(down_event)
    view_instance.handle_event(up_event)

    # Check that tab and selected item are updated
    assert view_instance._active_tab == "chip"
    assert view_instance._selected_item is None
    assert view_instance._data.chip_design_skill == 2


def test_item_selection(view: tuple[NewProjectView, Mock, Mock]):
    """Tests that clicking an item in the list selects it."""
    view_instance, _, _ = view

    assert view_instance._selected_item is None

    # Simulate a click on the first item in the list
    first_item_rect = view_instance._item_rects[0]
    # The event position needs to be relative to the view's surface
    click_pos = first_item_rect.center

    # The view's handle_event expects global coordinates
    global_click_pos = (
        click_pos[0] + view_instance.rect.x,
        click_pos[1] + view_instance.rect.y,
    )

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": global_click_pos}
    )
    view_instance.handle_event(event)

    assert view_instance._selected_item == "Sentry ICE"


def test_start_button_click(view: tuple[NewProjectView, Mock, Mock]):
    """Tests that the start button calls the on_start callback with correct data."""
    view_instance, on_start, _ = view

    # First, select an item and set a rating
    view_instance._selected_item = "Hammer"
    view_instance._rating_input.text = "3"

    # Find the start button and simulate a click
    start_button = [
        c
        for c in view_instance._components
        if isinstance(c, Button) and c.text == "Start"
    ][0]
    click_pos = start_button.rect.center
    global_click_pos = (
        click_pos[0] + view_instance.rect.x,
        click_pos[1] + view_instance.rect.y,
    )
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": global_click_pos}
    )
    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": global_click_pos}
    )
    view_instance.handle_event(down_event)
    view_instance.handle_event(up_event)

    on_start.assert_called_once_with("software", "Hammer", 3)


def test_start_button_click_no_item_selected(view: tuple[NewProjectView, Mock, Mock]):
    """Tests that the start button does nothing if no item is selected."""
    view_instance, on_start, _ = view

    # Ensure no item is selected and rating is valid
    view_instance._selected_item = None
    view_instance._rating_input.text = "3"

    # Call the handler directly to test its internal logic
    view_instance._handle_start_click()

    on_start.assert_not_called()


@pytest.mark.parametrize("invalid_rating", ["abc", "", "0", "-5"])
def test_start_button_click_invalid_rating(
    view: tuple[NewProjectView, Mock, Mock], invalid_rating: str
):
    """Tests the start button does nothing if the rating is not a positive integer."""
    view_instance, on_start, _ = view

    # Select an item but provide an invalid rating
    view_instance._selected_item = "Hammer"
    view_instance._rating_input.text = invalid_rating

    # Call the handler directly to test its internal logic
    view_instance._handle_start_click()

    on_start.assert_not_called()


def test_cancel_button_click(view: tuple[NewProjectView, Mock, Mock]):
    """Tests that the cancel button calls the on_close callback."""
    view_instance, _, on_close = view

    cancel_button = [
        c
        for c in view_instance._components
        if isinstance(c, Button) and c.text == "Cancel"
    ][0]
    click_pos = cancel_button.rect.center
    global_click_pos = (
        click_pos[0] + view_instance.rect.x,
        click_pos[1] + view_instance.rect.y,
    )
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": global_click_pos}
    )
    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": global_click_pos}
    )
    view_instance.handle_event(down_event)
    view_instance.handle_event(up_event)

    on_close.assert_called_once()
