import uuid
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import ContractSummaryDTO
from decker_pygame.domain.ids import ContractId
from decker_pygame.presentation.components.contract_list_view import (
    ContractListView,
)
from decker_pygame.presentation.components.list_view import ListView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_on_contract_selected() -> Mock:
    """Provides a mock callback for selection changes."""
    return Mock()


@pytest.fixture
def contract_list() -> list[ContractSummaryDTO]:
    """Provides a sample list of contracts."""
    return [
        ContractSummaryDTO(
            id=ContractId(uuid.uuid4()),
            title="Data Heist",
            client="Ares",
            reward=5000,
        ),
        ContractSummaryDTO(
            id=ContractId(uuid.uuid4()),
            title="Extraction",
            client="Aztechnology",
            reward=10000,
        ),
    ]


@patch(
    "decker_pygame.presentation.components.contract_list_view.ListView", spec=ListView
)
def test_contract_list_view_initialization(
    mock_list_view_class: Mock, mock_on_contract_selected: Mock
):
    """Tests that the ContractListView initializes and creates its child ListView."""
    pos = (10, 20)
    size = (400, 300)
    view = ContractListView(
        position=pos,
        size=size,
        on_contract_selected=mock_on_contract_selected,
    )

    assert view.rect.topleft == pos
    mock_list_view_class.assert_called_once()
    call_args = mock_list_view_class.call_args
    assert call_args.kwargs["position"] == (0, 0)
    assert call_args.kwargs["size"] == size
    assert call_args.kwargs["on_selection_change"] == mock_on_contract_selected


@patch(
    "decker_pygame.presentation.components.contract_list_view.ListView", spec=ListView
)
def test_set_contracts(
    mock_list_view_class: Mock,
    mock_on_contract_selected: Mock,
    contract_list: list[ContractSummaryDTO],
):
    """Tests that set_contracts calls the underlying ListView's set_items."""
    mock_list_view_instance = mock_list_view_class.return_value
    view = ContractListView((0, 0), (1, 1), mock_on_contract_selected)

    view.set_contracts(contract_list)

    mock_list_view_instance.set_items.assert_called_once_with(
        contract_list, view._contract_renderer
    )


@patch(
    "decker_pygame.presentation.components.contract_list_view.ListView", spec=ListView
)
def test_handle_event_delegation(
    mock_list_view_class: Mock, mock_on_contract_selected: Mock
):
    """Tests that handle_event delegates to the child ListView."""
    mock_list_view_instance = mock_list_view_class.return_value
    view = ContractListView((0, 0), (1, 1), mock_on_contract_selected)
    event = pygame.event.Event(pygame.USEREVENT)

    view.handle_event(event)

    mock_list_view_instance.handle_event.assert_called_once_with(event)


def test_contract_renderer_formats_correctly(contract_list: list[ContractSummaryDTO]):
    """Tests that the internal contract renderer formats data as expected."""
    # We need a real view to access its private renderer method
    view = ContractListView((0, 0), (1, 1), on_contract_selected=Mock())
    contract_to_render = contract_list[0]  # "Data Heist"

    rendered_strings = view._contract_renderer(contract_to_render)

    assert rendered_strings == ["Ares", "Data Heist", "$5000"]


@patch(
    "decker_pygame.presentation.components.contract_list_view.ListView", spec=ListView
)
def test_update_delegation(mock_list_view_class: Mock, mock_on_contract_selected: Mock):
    """Tests that the update method delegates to its child components."""
    view = ContractListView(
        (0, 0), (1, 1), on_contract_selected=mock_on_contract_selected
    )

    # The view's _components group contains the ListView instance.
    # We can patch the group's methods.
    with (
        patch.object(view._components, "update") as mock_update,
        patch.object(view._components, "draw") as mock_draw,
    ):
        view.update()

        mock_update.assert_called_once()
        mock_draw.assert_called_once_with(view.image)
