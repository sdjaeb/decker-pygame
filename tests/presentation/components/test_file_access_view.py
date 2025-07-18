"""Tests for the FileAccessView component."""

from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.application.dtos import FileAccessViewDTO, FileDTO
from decker_pygame.presentation.components.base_widgets import Clickable
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.file_access_view import FileAccessView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_callbacks() -> dict[str, Mock]:
    """Provides a dictionary of mock callback functions."""
    return {
        "on_close": Mock(),
        "on_download": Mock(),
        "on_delete": Mock(),
    }


@pytest.fixture
def file_access_data() -> FileAccessViewDTO:
    """Provides sample data for the FileAccessView."""
    return FileAccessViewDTO(
        node_name="Test Node",
        files=[
            FileDTO(name="file1.dat", size=100, file_type="Data"),
            FileDTO(name="file2.prg", size=200, file_type="Program"),
        ],
    )


@pytest.fixture
def file_access_view(
    file_access_data: FileAccessViewDTO,
    mock_callbacks: dict[str, Mock],
) -> FileAccessView:
    """Provides a FileAccessView instance for testing."""
    return FileAccessView(
        data=file_access_data,
        on_close=mock_callbacks["on_close"],
        on_download=mock_callbacks["on_download"],
        on_delete=mock_callbacks["on_delete"],
    )


def test_file_access_view_initialization(file_access_view: FileAccessView):
    """Tests that the view is initialized correctly."""
    assert file_access_view.rect.topleft == (100, 100)
    assert file_access_view.rect.size == (600, 400)

    # 1 title, 4 headers, 3 labels/file * 2 files,
    # 2 buttons/file * 2 files, 1 close button
    # 1 + 4 + 6 + 4 + 1 = 16 components
    assert len(file_access_view._components) == 16


def test_close_button_callback(
    file_access_view: FileAccessView, mock_callbacks: dict[str, Mock]
):
    """Tests that clicking the close button triggers the on_close callback."""
    # Use next() with a generator and isinstance to find the specific button.
    # This is more efficient and provides better type hints than a list comprehension.
    close_button = next(
        c
        for c in file_access_view._components
        if isinstance(c, Button) and c.text == "Close"
    )

    close_button._on_click()
    mock_callbacks["on_close"].assert_called_once()


def test_download_button_callbacks(
    file_access_view: FileAccessView, mock_callbacks: dict[str, Mock]
):
    """Tests that clicking download buttons triggers the on_download callback."""
    download_buttons = [
        c
        for c in file_access_view._components
        if isinstance(c, Button) and c.text == "Download"
    ]
    assert len(download_buttons) == 2

    # Click first download button
    download_buttons[0]._on_click()
    mock_callbacks["on_download"].assert_called_once_with("file1.dat")

    # Click second download button
    download_buttons[1]._on_click()
    mock_callbacks["on_download"].assert_called_with("file2.prg")
    assert mock_callbacks["on_download"].call_count == 2


def test_delete_button_callbacks(
    file_access_view: FileAccessView, mock_callbacks: dict[str, Mock]
):
    """Tests that clicking delete buttons triggers the on_delete callback."""
    delete_buttons = [
        c
        for c in file_access_view._components
        if isinstance(c, Button) and c.text == "Delete"
    ]
    assert len(delete_buttons) == 2

    # Click first delete button
    delete_buttons[0]._on_click()
    mock_callbacks["on_delete"].assert_called_once_with("file1.dat")

    # Click second delete button
    delete_buttons[1]._on_click()
    mock_callbacks["on_delete"].assert_called_with("file2.prg")
    assert mock_callbacks["on_delete"].call_count == 2


def test_handle_event_translates_mouse_pos(file_access_view: FileAccessView):
    """Tests that handle_event correctly translates mouse coordinates."""
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 120), "button": 1})
    # The mock must be a spec of a Clickable to be handled by the view.
    mock_component = Mock(spec=Clickable)
    file_access_view._components.add(mock_component)

    file_access_view.handle_event(event)

    # Assert the mock was called, then inspect the call.
    mock_component.handle_event.assert_called_once()
    call_args, _ = mock_component.handle_event.call_args
    translated_event = call_args[0]
    assert translated_event.pos == (50, 20)


def test_handle_event_non_mouse_event(file_access_view: FileAccessView):
    """Tests that non-mouse events are passed through without modification."""
    # Create a mock component that can handle events
    mock_component = Mock(spec=Clickable)
    file_access_view._components.add(mock_component)

    # Create a non-mouse event
    key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)

    # Act
    file_access_view.handle_event(key_event)

    # Assert that the original event was passed to the component
    mock_component.handle_event.assert_called_once_with(key_event)


def test_update_calls_components_update(file_access_view: FileAccessView):
    """Tests that the view's update method calls update on its children."""
    # Add a mock component to spy on
    mock_component = Mock(spec=pygame.sprite.Sprite)
    # The mock needs 'image' and 'rect' attributes for the draw() call to work.
    mock_component.image = pygame.Surface((1, 1))
    mock_component.rect = pygame.Rect(0, 0, 1, 1)
    file_access_view._components.add(mock_component)

    # Call the update method
    file_access_view.update()

    # Assert that the mock component's update method was called
    mock_component.update.assert_called_once()
