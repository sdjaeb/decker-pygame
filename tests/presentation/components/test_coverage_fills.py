from unittest.mock import Mock, patch

import pygame

from decker_pygame.presentation.components.active_bar import ActiveBar
from decker_pygame.presentation.components.mission_results_view import (
    MissionResultsView,
)
from decker_pygame.settings import GFX, UI_FACE


def test_active_bar_remove_existing_program_and_update():
    pygame.init()
    try:
        icon_size = GFX.active_bar_image_size
        image_list = [pygame.Surface((icon_size, icon_size)) for _ in range(5)]
        for i, img in enumerate(image_list):
            img.fill((i + 1, 0, 0))

        bar = ActiveBar(position=(0, 0), image_list=image_list)

        # Directly inject a program into the internal mapping to hit the
        # code path where remove_program finds the slot and deletes it.
        bar.active_programs[0] = 2
        bar.update()
        assert 2 in bar.active_programs.values()

        bar.remove_program(2)
        assert 2 not in bar.active_programs.values()

        # After removal, the slot should render as UI_FACE again
        assert bar.image.get_at((0, 0)) == UI_FACE
    finally:
        pygame.quit()


def test_mission_results_call_create_and_render_directly():
    pygame.init()
    try:
        mock_on_close = Mock()

        with (
            patch("pygame.font.Font") as mock_font_class,
            patch(
                "decker_pygame.presentation.components.mission_results_view.Button"
            ) as mock_button_class,
        ):
            mock_font_instance = Mock()
            mock_font_instance.render.return_value = pygame.Surface((50, 10))
            mock_font_instance.get_linesize.return_value = 10
            mock_font_class.return_value = mock_font_instance

            class DummyButton(pygame.sprite.Sprite):
                def __init__(self):
                    super().__init__()
                    self.image = pygame.Surface((10, 10))
                    self.rect = pygame.Rect(0, 0, 10, 10)

                def handle_event(self, event):
                    return None

            mock_button_class.return_value = DummyButton()

            # Create the view and then explicitly call helper methods to
            # ensure those code regions are executed.
            view = MissionResultsView(
                data=Mock(
                    was_successful=True,
                    contract_name="x",
                    credits_earned=1,
                    reputation_change=0,
                ),
                on_close=mock_on_close,
            )

            # Call helpers directly
            view._create_widgets()
            view._render()
    finally:
        pygame.quit()
