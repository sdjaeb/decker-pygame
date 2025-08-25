"""Tests for the concrete game state classes and their base protocol."""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pygame

from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.matrix_run_view import MatrixRunView
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.states.game_states import BaseState
from decker_pygame.presentation.states.states import (
    HomeState,
    IntroState,
    MatrixRunState,
    NewCharState,
)

if TYPE_CHECKING:
    from decker_pygame.presentation.game import Game


class DummyState(BaseState):
    """A concrete class for testing the BaseState protocol for coverage."""

    def __init__(self, game: "Game") -> None:
        """Initializes the dummy state."""

    def on_enter(self) -> None:
        """Dummy on_enter."""

    def on_exit(self) -> None:
        """Dummy on_exit."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Dummy handle_event."""

    def update(self, dt: float) -> None:
        """Dummy update."""

    def draw(self, screen: pygame.Surface) -> None:
        """Dummy draw."""


def test_base_state_protocol_coverage() -> None:
    """This test exists purely to satisfy coverage for the protocol definition."""
    mock_game = Mock()
    state = DummyState(mock_game)
    state.on_enter()
    state.on_exit()
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.1)
    state.draw(Mock(spec=pygame.Surface))


def test_intro_state_lifecycle() -> None:
    """Tests that IntroState correctly toggles the IntroView via the ViewManager."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = IntroState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "intro_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.IntroView", spec=IntroView
    ) as mock_intro_view_class:
        created_view = factory_arg()
        mock_intro_view_class.assert_called_once_with(
            on_continue=mock_game._continue_from_intro
        )
        assert created_view is mock_intro_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "intro_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)


def test_new_char_state_lifecycle() -> None:
    """Tests that NewCharState correctly toggles the NewCharView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = NewCharState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "new_char_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.NewCharView", spec=NewCharView
    ) as mock_view_class:
        created_view = factory_arg()
        mock_view_class.assert_called_once_with(
            on_create=mock_game._handle_character_creation
        )
        assert created_view is mock_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "new_char_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)


def test_home_state_lifecycle() -> None:
    """Tests that HomeState correctly toggles the HomeView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = HomeState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "home_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.HomeView", spec=HomeView
    ) as mock_view_class:
        created_view = factory_arg()
        mock_view_class.assert_called_once_with(
            on_char=mock_game.toggle_char_data_view,
            on_deck=mock_game.toggle_deck_view,
            on_contracts=mock_game.toggle_contract_list_view,
            on_build=mock_game.toggle_build_view,
            on_shop=mock_game.toggle_shop_view,
            on_transfer=mock_game.toggle_transfer_view,
            on_projects=mock_game.toggle_project_data_view,
        )
        assert created_view is mock_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "home_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)


def test_matrix_run_state_lifecycle() -> None:
    """Tests that MatrixRunState correctly toggles the MatrixRunView."""
    mock_game = Mock()
    mock_game.view_manager = Mock()
    state = MatrixRunState(mock_game)

    # --- Test on_enter ---
    state.on_enter()
    mock_game.view_manager.toggle_view.assert_called_once()

    # Check the arguments passed to toggle_view
    view_attr_arg = mock_game.view_manager.toggle_view.call_args.args[0]
    factory_arg = mock_game.view_manager.toggle_view.call_args.args[1]
    assert view_attr_arg == "matrix_run_view"

    # Test the factory function itself
    with patch(
        "decker_pygame.presentation.states.states.MatrixRunView", spec=MatrixRunView
    ) as mock_view_class:
        created_view = factory_arg()
        mock_view_class.assert_called_once_with(asset_service=mock_game.asset_service)
        assert created_view is mock_view_class.return_value

    # --- Test on_exit ---
    mock_game.view_manager.reset_mock()
    state.on_exit()
    mock_game.view_manager.toggle_view.assert_called_once_with(
        "matrix_run_view", state._factory
    )

    # --- Test update, draw, and event handling delegation ---
    state.handle_event(pygame.event.Event(pygame.USEREVENT))
    state.update(0.016)
    mock_game.update_sprites.assert_called_once_with(0.016)
    mock_screen = Mock(spec=pygame.Surface)
    state.draw(mock_screen)
    mock_game.all_sprites.draw.assert_called_once_with(mock_screen)
