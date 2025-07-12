from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.character_service import CharacterViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.char_data_view import CharDataView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_char_data_view_initialization():
    """Tests that the CharDataView initializes and renders its data."""
    mock_on_close = Mock()
    mock_inc_skill = Mock()
    mock_dec_skill = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.char_data_view.Button"
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        # Make the mock render return a surface with a width, needed for layout
        mock_render_surface = pygame.Surface((50, 20))
        mock_font_instance.render.return_value = mock_render_surface
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        # We need to provide mock instances for each button created
        # 3 main buttons + 2 increase buttons + 2 decrease buttons
        mock_button_instances = [Mock(spec=Button) for _ in range(7)]
        for inst in mock_button_instances:
            inst.image = pygame.Surface((10, 10))
            inst.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.side_effect = mock_button_instances

        view_data = CharacterViewData(
            name="Testy",
            reputation=10,
            credits=1234,
            health=88,
            skills={"hacking": 5, "crafting": 2},
            unused_skill_points=10,
        )

        view = CharDataView(
            position=(10, 20),
            data=view_data,
            on_close=mock_on_close,
            on_increase_skill=mock_inc_skill,
            on_decrease_skill=mock_dec_skill,
        )

        assert view.rect.topleft == (10, 20)
        # Check that all data lines were rendered
        # 4 info lines + 1 skills header + 2 skill labels + 2 skill values
        assert mock_font_instance.render.call_count == 9
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]
        assert "Name: Testy" in rendered_texts
        assert "Reputation: 10" in rendered_texts
        assert "Money: $1234" in rendered_texts
        assert "Health: 88%" in rendered_texts
        assert "Skills: (Points Available: 10)" in rendered_texts
        assert "  Hacking:" in rendered_texts
        assert "  Crafting:" in rendered_texts
        assert "5" in rendered_texts
        assert "2" in rendered_texts

        # Check that all buttons were created and added to components
        assert mock_button_class.call_count == 7
        assert view._view_deck_button is mock_button_instances[0]
        assert view._upgrade_lifestyle_button is mock_button_instances[1]
        assert view._close_button is mock_button_instances[2]
        assert len(view._components) == 7


def test_char_data_view_close_button_click():
    """Tests that the view correctly delegates events to its child button."""
    mock_on_close = Mock()
    mock_inc_skill = Mock()
    mock_dec_skill = Mock()
    with patch(
        "decker_pygame.presentation.components.char_data_view.Button"
    ) as mock_button_class:
        # We need to provide mock instances for each button created
        # 3 main buttons + 1 increase + 1 decrease
        mock_button_instances = [Mock(spec=Button) for _ in range(5)]
        for inst in mock_button_instances:
            inst.image = pygame.Surface((10, 10))
            inst.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.side_effect = mock_button_instances

        view_data = CharacterViewData(
            name="Testy",
            reputation=10,
            credits=1234,
            health=88,
            skills={"hacking": 5},
            unused_skill_points=10,
        )
        view = CharDataView(
            position=(50, 50),
            data=view_data,
            on_close=mock_on_close,
            on_increase_skill=mock_inc_skill,
            on_decrease_skill=mock_dec_skill,
        )

        # Create an event with screen-space coordinates
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
        )

        view.handle_event(event)

        # Assert that all buttons' handle_event was called with a new event
        # that has translated, view-local coordinates.
        for inst in mock_button_instances:
            inst.handle_event.assert_called_once()
            called_event = inst.handle_event.call_args.args[0]
            assert isinstance(called_event, pygame.event.Event)
            assert called_event.pos == (50, 50)  # 100-50, 100-50
