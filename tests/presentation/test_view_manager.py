"""Tests for the ViewManager class."""

from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.protocols import Eventful
from decker_pygame.presentation.view_manager import ViewManager


class MockEventfulSprite(pygame.sprite.Sprite, Eventful):
    """A dummy view class that is both a Sprite and Eventful for testing."""

    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.image = pygame.Surface((10, 10))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events."""


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object."""
    game = Mock()
    game.all_sprites = Mock(spec=pygame.sprite.Group)
    # Set the view attribute to None initially
    game.test_view = None
    return game


@pytest.fixture
def view_manager(mock_game: Mock) -> ViewManager:
    """Provides a ViewManager instance initialized with a mock game."""
    return ViewManager(mock_game)


def test_view_manager_initialization(
    view_manager: ViewManager, mock_game: Mock
) -> None:
    """Tests that the ViewManager initializes correctly."""
    assert view_manager._game is mock_game
    assert view_manager.modal_stack == []


def test_toggle_view_opens_view(view_manager: ViewManager, mock_game: Mock) -> None:
    """Tests opening a view that is currently closed."""
    mock_view_instance = Mock(spec=MockEventfulSprite)
    mock_view_factory = Mock(return_value=mock_view_instance)

    view_manager.toggle_view("test_view", mock_view_factory)

    mock_view_factory.assert_called_once()
    assert mock_game.test_view is mock_view_instance
    mock_game.all_sprites.add.assert_called_once_with(mock_view_instance)
    assert view_manager.modal_stack == [mock_view_instance]


def test_toggle_view_closes_view(view_manager: ViewManager, mock_game: Mock) -> None:
    """Tests closing a view that is currently open."""
    mock_view_instance = Mock(spec=MockEventfulSprite)
    mock_game.test_view = mock_view_instance
    view_manager.modal_stack.append(mock_view_instance)
    mock_view_factory = Mock()

    view_manager.toggle_view("test_view", mock_view_factory)

    mock_view_factory.assert_not_called()
    assert mock_game.test_view is None
    mock_game.all_sprites.remove.assert_called_once_with(mock_view_instance)
    assert not view_manager.modal_stack


def test_toggle_view_factory_returns_none(
    view_manager: ViewManager, mock_game: Mock
) -> None:
    """Tests that nothing happens if the view factory returns None."""
    mock_view_factory = Mock(return_value=None)
    view_manager.toggle_view("test_view", mock_view_factory)
    assert mock_game.test_view is None
    mock_game.all_sprites.add.assert_not_called()


def test_toggle_view_non_eventful(view_manager: ViewManager, mock_game: Mock) -> None:
    """Tests that a non-eventful view is not added to the modal stack."""
    mock_view_instance = Mock(spec=pygame.sprite.Sprite)
    delattr(mock_view_instance, "handle_event")
    mock_view_factory = Mock(return_value=mock_view_instance)
    view_manager.toggle_view("test_view", mock_view_factory)
    assert not view_manager.modal_stack
