from unittest.mock import Mock, patch
from uuid import uuid4

import pygame
import pytest

from decker_pygame.application.dtos import ContractSummaryDTO
from decker_pygame.domain.ids import ContractId
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.contract_data_view import ContractDataView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_contract() -> Mock:
    """Provides a mock ContractSummaryDTO."""
    mock_dto = Mock(spec=ContractSummaryDTO)
    mock_dto.id = ContractId(uuid4())
    mock_dto.title = "Test Contract"
    mock_dto.client = "Test Client"
    mock_dto.reward = 1000
    return mock_dto


def test_contract_data_view_initialization(mock_contract: Mock):
    """Tests that the ContractDataView initializes and renders its data."""
    mock_on_accept = Mock()
    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.contract_data_view.Button",
            spec=Button,
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_class.return_value = mock_font_instance

        # The mock button needs a real surface for the .image attribute
        # to be blitted by the sprite group's draw() method.
        mock_button_instance = mock_button_class.return_value
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)

        view = ContractDataView(
            position=(10, 20),
            size=(300, 200),
            contract=mock_contract,
            on_accept=mock_on_accept,
        )

        assert view.rect.topleft == (10, 20)
        # Check that it renders the contract details
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]
        assert f"Title: {mock_contract.title}" in rendered_texts
        assert f"Client: {mock_contract.client}" in rendered_texts
        assert f"Reward: ${mock_contract.reward}" in rendered_texts

        # Check that the accept button was created
        mock_button_class.assert_called_once()


def test_contract_data_view_handles_event(mock_contract: Mock):
    """Tests that the view's handle_event method runs without error."""
    mock_on_accept = Mock()
    with patch(
        "decker_pygame.presentation.components.contract_data_view.Button", spec=Button
    ) as mock_button_class:
        mock_button_instance = mock_button_class.return_value
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        view = ContractDataView(
            position=(10, 20),
            size=(300, 200),
            contract=mock_contract,
            on_accept=mock_on_accept,
        )
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(15, 25))
        view.handle_event(event)

        # Check that the event was passed to the button's handler
        mock_button_instance.handle_event.assert_called_once()
