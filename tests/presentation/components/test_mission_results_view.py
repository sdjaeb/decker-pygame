from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import MissionResultsDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.mission_results_view import (
    MissionResultsView,
)


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def success_data():
    return MissionResultsDTO(
        contract_name="Data Heist",
        was_successful=True,
        credits_earned=5000,
        reputation_change=1,
    )


@pytest.fixture
def failure_data():
    return MissionResultsDTO(
        contract_name="Corp Infiltration",
        was_successful=False,
        credits_earned=0,
        reputation_change=-1,
    )


def test_mission_results_view_initialization_success(success_data):
    """Tests that the view initializes and renders success data correctly."""
    mock_on_close = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.mission_results_view.Button"
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        mock_button_instance = Mock(spec=Button)
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.return_value = mock_button_instance

        view = MissionResultsView(data=success_data, on_close=mock_on_close)

        assert view is not None
        # Title + 4 lines of data
        assert mock_font_instance.render.call_count == 5
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]

        assert "Status: Success" in rendered_texts
        assert "Reputation Change: +1" in rendered_texts

        mock_button_class.assert_called_once()


def test_mission_results_view_initialization_failure(failure_data):
    """Tests that the view initializes and renders failure data correctly."""
    mock_on_close = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch("decker_pygame.presentation.components.mission_results_view.Button"),
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        MissionResultsView(data=failure_data, on_close=mock_on_close)

        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]

        assert "Status: Failure" in rendered_texts
        assert "Reputation Change: -1" in rendered_texts


def test_mission_results_view_event_handling(success_data):
    """Tests that the view correctly delegates events to its components."""
    mock_on_close = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.mission_results_view.Button"
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        mock_button_instance = Mock(spec=Button)
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.return_value = mock_button_instance

        view = MissionResultsView(data=success_data, on_close=mock_on_close)

        with patch.object(
            view._components.sprites()[0], "handle_event"
        ) as mock_button_handler:
            event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}
            )
            view.handle_event(event)
            mock_button_handler.assert_called_once()
