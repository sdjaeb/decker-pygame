from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.components.list_view import ListView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def sample_list_data():
    """Provides sample data for the ListView."""
    return [
        {"id": 1, "name": "Item A", "value": 10},
        {"id": 2, "name": "Item B", "value": 20},
        {"id": 3, "name": "Item C", "value": 30},
    ]


@pytest.fixture
def mock_on_selection_change():
    """Provides a mock callback for selection changes."""
    return Mock()


@pytest.fixture
def list_view_instance(mock_on_selection_change):
    """Provides a ListView instance for testing."""
    columns = [("Name", 100), ("Value", 50)]
    return ListView((0, 0), (200, 150), columns, mock_on_selection_change)


def test_list_view_initialization(list_view_instance):
    """Tests that the ListView initializes correctly."""
    assert list_view_instance.rect.size == (200, 150)
    assert list_view_instance._selected_index is None


def test_set_items_renders_items_and_resets_selection(
    list_view_instance, sample_list_data, mock_on_selection_change
):
    """
    Tests that set_items correctly populates and renders the list, and resets selection.
    """

    def item_renderer(item):
        return [item["name"], str(item["value"])]

    list_view_instance.set_items(sample_list_data, item_renderer)

    assert list_view_instance._items == sample_list_data
    assert list_view_instance._item_renderer == item_renderer
    assert list_view_instance._selected_index is None
    mock_on_selection_change.assert_called_once_with(None)  # Initial reset

    # Verify that item rects are created (implies rendering)
    assert len(list_view_instance._item_rects) == len(sample_list_data)
    for rect in list_view_instance._item_rects:
        assert isinstance(rect, pygame.Rect)


def test_handle_event_selects_item(
    list_view_instance, sample_list_data, mock_on_selection_change
):
    """
    Tests that clicking an item selects it and triggers the callback.
    """

    def item_renderer(item):
        return [item["name"], str(item["value"])]

    list_view_instance.set_items(sample_list_data, item_renderer)
    mock_on_selection_change.reset_mock()  # Reset after initial set_items call

    # Simulate click on the first item
    first_item_rect = list_view_instance._item_rects[0]
    click_pos = first_item_rect.center
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos})
    list_view_instance.handle_event(event)

    assert list_view_instance._selected_index == 0
    mock_on_selection_change.assert_called_once_with(sample_list_data[0])


def test_handle_event_changes_selection(
    list_view_instance, sample_list_data, mock_on_selection_change
):
    """
    Tests that clicking a different item changes the selection.
    """

    def item_renderer(item):
        return [item["name"], str(item["value"])]

    list_view_instance.set_items(sample_list_data, item_renderer)
    mock_on_selection_change.reset_mock()

    # Select first item
    first_item_rect = list_view_instance._item_rects[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": first_item_rect.center}
    )
    list_view_instance.handle_event(event)
    mock_on_selection_change.reset_mock()

    # Select second item
    second_item_rect = list_view_instance._item_rects[1]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": second_item_rect.center}
    )
    list_view_instance.handle_event(event)

    assert list_view_instance._selected_index == 1
    mock_on_selection_change.assert_called_once_with(sample_list_data[1])


def test_handle_event_deselects_item_on_click_outside_item(
    list_view_instance, sample_list_data, mock_on_selection_change
):
    """
    Tests that clicking outside an item (but within the list view) deselects it.
    """

    def item_renderer(item):
        return [item["name"], str(item["value"])]

    list_view_instance.set_items(sample_list_data, item_renderer)
    mock_on_selection_change.reset_mock()

    # Select first item
    first_item_rect = list_view_instance._item_rects[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": first_item_rect.center}
    )
    list_view_instance.handle_event(event)
    mock_on_selection_change.reset_mock()

    # Click within the list view but not on any item (e.g., below the last item)
    click_pos = (
        list_view_instance.rect.x + 10,
        list_view_instance.rect.y + list_view_instance.rect.height - 5,
    )
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos})
    list_view_instance.handle_event(event)

    assert list_view_instance._selected_index is None
    mock_on_selection_change.assert_called_once_with(None)


def test_handle_event_no_change_on_click_same_item(
    list_view_instance, sample_list_data, mock_on_selection_change
):
    """
    Tests that clicking the same item does not trigger a selection change callback.
    """

    def item_renderer(item):
        return [item["name"], str(item["value"])]

    list_view_instance.set_items(sample_list_data, item_renderer)
    mock_on_selection_change.reset_mock()

    # Select first item
    first_item_rect = list_view_instance._item_rects[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": first_item_rect.center}
    )
    list_view_instance.handle_event(event)
    mock_on_selection_change.reset_mock()

    # Click the same item again
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": first_item_rect.center}
    )
    list_view_instance.handle_event(event)

    assert list_view_instance._selected_index == 0
    mock_on_selection_change.assert_not_called()


def test_handle_event_no_change_on_click_outside_list_view(
    list_view_instance, sample_list_data, mock_on_selection_change
):
    """
    Tests that clicking outside the list view does not affect selection.
    """

    def item_renderer(item):
        return [item["name"], str(item["value"])]

    list_view_instance.set_items(sample_list_data, item_renderer)
    mock_on_selection_change.reset_mock()

    # Select first item
    first_item_rect = list_view_instance._item_rects[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": first_item_rect.center}
    )
    list_view_instance.handle_event(event)
    mock_on_selection_change.reset_mock()

    # Click outside the list view
    click_pos = (
        list_view_instance.rect.x + list_view_instance.rect.width + 10,
        list_view_instance.rect.y + 10,
    )
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos})
    list_view_instance.handle_event(event)

    assert list_view_instance._selected_index == 0  # Selection should remain unchanged
    mock_on_selection_change.assert_not_called()
