from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.text_input import TextInput


@pytest.fixture(autouse=True)
def pygame_context():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def text_input():
    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((50, 20))
        mock_font_class.return_value = mock_font_instance
        yield TextInput((100, 100), (200, 30), "Name:", "Decker")


def test_text_input_initialization(text_input: TextInput):
    assert text_input.text == "Decker"
    assert text_input.rect.topleft == (100, 100)
    assert text_input.rect.size == (200, 30)
    assert not text_input._active


def test_text_input_activation_on_click(text_input: TextInput):
    # Click inside
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 115)})
    text_input.handle_event(event)
    assert text_input._active

    # Click inside again (toggles off)
    text_input.handle_event(event)
    assert not text_input._active


def test_text_input_deactivation_on_click_outside(text_input: TextInput):
    # Activate first
    text_input._active = True

    # Click outside
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
    text_input.handle_event(event)
    assert not text_input._active


def test_text_input_handles_keydown_when_active(text_input: TextInput):
    text_input._active = True

    # Type a character
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "a"})
    text_input.handle_event(event)
    assert text_input.text == "Deckera"

    # Use backspace
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
    text_input.handle_event(event)
    assert text_input.text == "Decker"


def test_text_input_ignores_keydown_when_inactive(text_input: TextInput):
    text_input._active = False

    # Type a character
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "a"})
    text_input.handle_event(event)
    assert text_input.text == "Decker"

    # Use backspace
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
    text_input.handle_event(event)
    assert text_input.text == "Decker"
