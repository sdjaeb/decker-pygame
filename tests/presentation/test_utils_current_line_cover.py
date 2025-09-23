from unittest.mock import Mock

import pygame


def test_render_text_wrapped_executes_empty_current_line():
    """Ensure the code path that assigns an empty current_line runs.

    We force max_width to be smaller than a single character so the
    chunk-building loop never accumulates a character and `chunk` stays
    empty, hitting the `current_line = ""` branch.
    """
    pygame.init()
    try:
        from decker_pygame.presentation.utils import render_text_wrapped

        # Font where each char is 10px wide
        font = Mock()
        font.size.side_effect = lambda s: (len(s) * 10, 10)
        font.get_linesize.return_value = 10
        font.render.return_value = pygame.Surface((1, 1))

        surface = pygame.Surface((10, 10))
        # rect width set to 5 makes max_width = 5 -> less than a single char
        rect = pygame.Rect(0, 0, 5, 10)

        # Long unbreakable word to force chunking
        render_text_wrapped(
            surface=surface,
            text="A_very_long_unbreakable_word",
            font=font,
            color=pygame.Color("white"),
            rect=rect,
            padding=0,
        )

        # Verify rendering was attempted at least once
        assert font.render.call_count >= 1
    finally:
        pygame.quit()
