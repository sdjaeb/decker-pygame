from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.presentation.components.build_view import BuildView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def schematics_list() -> list[Schematic]:
    """Provides a sample list of schematics for testing."""
    return [
        Schematic(
            name="IcePick v1",
            produces_item_name="IcePick v1",
            produces_item_size=10,
            cost=[RequiredResource(name="credits", quantity=500)],
        ),
        Schematic(
            name="Hammer",
            produces_item_name="Hammer",
            produces_item_size=20,
            cost=[RequiredResource(name="credits", quantity=1000)],
        ),
    ]


def test_build_view_initialization(schematics_list: list[Schematic]):
    """Tests that the BuildView initializes and renders its schematics."""
    mock_callback = Mock()

    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        view = BuildView(
            position=(10, 20),
            size=(300, 200),
            schematics=schematics_list,
            on_build_click=mock_callback,
        )

        assert view.rect.topleft == (10, 20)
        assert mock_font_instance.render.call_count == 2
        assert len(view._schematic_rects) == 2


def test_build_view_click_handler(schematics_list: list[Schematic]):
    """Tests that clicking a schematic triggers the callback with the correct name."""
    mock_callback = Mock()
    view = BuildView(
        position=(100, 100),
        size=(400, 300),
        schematics=schematics_list,
        on_build_click=mock_callback,
    )

    # Simulate a click on the first schematic's rect.
    # The rect's absolute position is its relative position + the view's position.
    first_schematic_rect = view._schematic_rects[0]
    click_pos = (
        first_schematic_rect.centerx + view.rect.x,
        first_schematic_rect.centery + view.rect.y,
    )
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos})

    view.handle_event(event)

    mock_callback.assert_called_once_with("IcePick v1")
