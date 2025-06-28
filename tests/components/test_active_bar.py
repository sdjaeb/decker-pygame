import os
import pygame
import pytest
from typing import Iterator

from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.settings import GFX, UI_FACE

# --- Test Fixtures ---

@pytest.fixture(scope="module")
def pygame_display() -> Iterator[None]:
    """Fixture to initialize and quit pygame for tests that need a display."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    # A display is required for surface creation, even a dummy one.
    # Pylance flags this as an error because `set_mode` is loaded dynamically.
    pygame.display.set_mode((1, 1))  # type: ignore[attr-defined]
    yield
    pygame.quit()


@pytest.fixture
def mock_icon_surfaces(pygame_display: None) -> list[pygame.Surface]:
    """Creates a list of simple, colored surfaces to act as mock icons."""
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    size = (GFX.active_bar_image_size, GFX.active_bar_image_size)

    def create_surface(color):
        s = pygame.Surface(size)
        s.fill(color)
        return s

    return [create_surface(c) for c in colors]


@pytest.fixture
def active_bar(mock_icon_surfaces: list[pygame.Surface]) -> ActiveBar:
    """Creates a default ActiveBar instance for testing."""
    return ActiveBar(position=(0, 0), image_list=mock_icon_surfaces)


# --- Test Cases ---

def test_initialization(active_bar: ActiveBar):
    """Verify that the ActiveBar is initialized with correct default values."""
    expected_width = GFX.active_bar_image_size * GFX.active_bar_max_slots
    expected_height = GFX.active_bar_image_size

    assert active_bar.image.get_size() == (expected_width, expected_height)
    assert active_bar.rect.topleft == (0, 0)
    assert len(active_bar._active_slots) == GFX.active_bar_max_slots
    expected_slots = [False] * GFX.active_bar_max_slots
    assert active_bar._active_slots == expected_slots


def test_set_active_program_valid_slot(active_bar: ActiveBar):
    """Test activating a program in a valid slot."""
    slot_index = 2
    image_index = 1

    active_bar.set_active_program(slot_index, image_index)

    assert active_bar._active_slots[slot_index] is True
    assert active_bar._image_indices[slot_index] == image_index


@pytest.mark.parametrize("invalid_slot", [GFX.active_bar_max_slots, -1])
def test_set_active_program_invalid_slot(active_bar: ActiveBar, invalid_slot: int):
    """Test that attempting to activate a program in an invalid slot does nothing."""
    initial_slots_state = list(active_bar._active_slots)
    initial_indices_state = list(active_bar._image_indices)

    active_bar.set_active_program(invalid_slot, 0)

    assert active_bar._active_slots == initial_slots_state
    assert active_bar._image_indices == initial_indices_state


@pytest.mark.parametrize(
    "slot_index, image_index",
    [(0, 0), (GFX.active_bar_max_slots - 1, 1), (3, 2)],  # Test first, last, and a middle slot
)
def test_update_draws_active_icon(
    active_bar: ActiveBar,
    mock_icon_surfaces: list[pygame.Surface],
    slot_index: int,
    image_index: int,
):
    """Verify that the update method correctly draws an active icon onto the bar's surface."""
    icon_color = mock_icon_surfaces[image_index].get_at((0, 0))

    active_bar.set_active_program(slot_index, image_index)
    active_bar.update()

    # Check the pixel color where the icon should be drawn
    draw_x = slot_index * GFX.active_bar_image_size
    pixel_color = active_bar.image.get_at((draw_x, 0))
    assert pixel_color == icon_color

    # Check the pixel color of an empty slot to ensure it's the background color
    # If we drew on slot 0, check slot 1 for the background. Otherwise, check slot 0.
    empty_slot_index = 1 if slot_index == 0 else 0
    empty_slot_x = empty_slot_index * GFX.active_bar_image_size
    background_color_at_empty_slot = active_bar.image.get_at((empty_slot_x, 0))
    assert background_color_at_empty_slot == UI_FACE