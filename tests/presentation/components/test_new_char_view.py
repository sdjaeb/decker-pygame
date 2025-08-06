from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.components.text_input import TextInput


@pytest.fixture(autouse=True)
def pygame_context():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def new_char_view():
    mock_on_create = Mock()
    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.new_char_view.TextInput"
        ) as mock_text_input_class,
        patch(
            "decker_pygame.presentation.components.new_char_view.Button"
        ) as mock_button_class,
    ):
        mock_font_class.return_value.render.return_value = pygame.Surface((10, 10))

        mock_text_input_instance = Mock(spec=TextInput)
        mock_text_input_instance.image = pygame.Surface((10, 10))
        mock_text_input_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_text_input_instance.text = "TestName"
        mock_text_input_class.return_value = mock_text_input_instance

        mock_button_instance = Mock(spec=Button)
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.return_value = mock_button_instance

        view = NewCharView(on_create=mock_on_create)
        yield view, mock_on_create, mock_text_input_instance, mock_button_instance


def test_new_char_view_initialization(new_char_view):
    view, _, mock_text_input, mock_button = new_char_view
    assert view is not None
    assert mock_text_input in view._components
    assert mock_button in view._components


def test_new_char_view_create_click(new_char_view):
    view, mock_on_create, mock_text_input, _ = new_char_view
    mock_text_input.text = "Cassidy"

    view._handle_create_click()

    mock_on_create.assert_called_once_with("Cassidy")


def test_new_char_view_create_click_empty_name(new_char_view):
    view, mock_on_create, mock_text_input, _ = new_char_view
    mock_text_input.text = ""

    view._handle_create_click()

    mock_on_create.assert_not_called()


def test_new_char_view_event_handling(new_char_view):
    view, _, mock_text_input, mock_button = new_char_view
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (10, 10)})
    view.handle_event(event)
    mock_text_input.handle_event.assert_called_once()
    mock_button.handle_event.assert_called_once()
