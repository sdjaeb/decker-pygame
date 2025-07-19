"""Tests for the SoundEditView component."""

from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.application.dtos import SoundEditViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.slider import Slider
from decker_pygame.presentation.components.sound_edit_view import SoundEditView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_callbacks() -> dict[str, Mock]:
    """Provides a dictionary of mock callback functions."""
    return {
        "on_close": Mock(),
        "on_master_volume_change": Mock(),
        "on_music_volume_change": Mock(),
        "on_sfx_volume_change": Mock(),
    }


@pytest.fixture
def sound_view_data() -> SoundEditViewDTO:
    """Provides sample data for the SoundEditView."""
    return SoundEditViewDTO(master_volume=1.0, music_volume=0.5, sfx_volume=0.75)


@pytest.fixture
def sound_edit_view(
    sound_view_data: SoundEditViewDTO, mock_callbacks: dict[str, Mock]
) -> SoundEditView:
    """Provides a SoundEditView instance for testing."""
    return SoundEditView(
        data=sound_view_data,
        on_close=mock_callbacks["on_close"],
        on_master_volume_change=mock_callbacks["on_master_volume_change"],
        on_music_volume_change=mock_callbacks["on_music_volume_change"],
        on_sfx_volume_change=mock_callbacks["on_sfx_volume_change"],
    )


def test_sound_edit_view_initialization(sound_edit_view: SoundEditView):
    """Tests that the view is initialized correctly."""
    assert sound_edit_view.rect.topleft == (250, 250)
    # 3 labels, 3 sliders, 1 button
    assert len(sound_edit_view._components) == 7

    sliders = [c for c in sound_edit_view._components if isinstance(c, Slider)]
    assert sliders[0].value == 1.0  # Master
    assert sliders[1].value == 0.5  # Music
    assert sliders[2].value == 0.75  # SFX


def test_close_button_callback(
    sound_edit_view: SoundEditView, mock_callbacks: dict[str, Mock]
):
    """Tests that clicking the Close button triggers the on_close callback."""
    close_button = next(c for c in sound_edit_view._components if isinstance(c, Button))
    close_button._on_click()
    mock_callbacks["on_close"].assert_called_once()


def test_slider_callbacks(
    sound_edit_view: SoundEditView, mock_callbacks: dict[str, Mock]
):
    """Tests that clicking a slider triggers the correct callback with a new value."""
    sliders = [c for c in sound_edit_view._components if isinstance(c, Slider)]
    music_slider = sliders[1]

    # To get a predictable value, we calculate the exact click position needed.
    # We want to click at a position that corresponds to 25% of the slider's value.
    # The slider's value is based on its track width (total width - handle width).
    track_width = music_slider.rect.width - music_slider._handle_width
    target_x_in_slider = track_width * 0.25

    # Now calculate the absolute screen position for the event
    click_pos_local_to_view = (
        music_slider.rect.left + target_x_in_slider,
        music_slider.rect.centery,
    )
    click_pos_screen = sound_edit_view.rect.move(click_pos_local_to_view).topleft

    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos_screen}
    )

    # The event must be handled by the parent view, which translates coordinates.
    sound_edit_view.handle_event(down_event)

    mock_callbacks["on_music_volume_change"].assert_called_once()
    # The value should be approximately 0.25.
    assert mock_callbacks["on_music_volume_change"].call_args[0][0] == pytest.approx(
        0.25
    )


def test_sound_edit_view_update(sound_edit_view: SoundEditView):
    """Tests that the update method calls update on its children."""
    # Add a mock component to spy on
    mock_component = Mock(spec=pygame.sprite.Sprite)
    # The mock needs 'image' and 'rect' attributes for the draw() call to work.
    mock_component.image = pygame.Surface((1, 1))
    mock_component.rect = pygame.Rect(0, 0, 1, 1)
    sound_edit_view._components.add(mock_component)

    # Call the update method
    sound_edit_view.update()

    # Assert that the mock component's update method was called
    mock_component.update.assert_called_once()
