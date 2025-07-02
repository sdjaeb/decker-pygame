import pygame

from decker_pygame.presentation.components.active_bar import ActiveBar
from decker_pygame.settings import GFX, UI_FACE


class TestActiveBar:
    def test_initialization(self):
        pygame.init()

        # The image_list should contain images of the correct size as defined
        # in settings. The number of icons in the source sheet doesn't determine
        # the bar's final size.
        icon_size = GFX.active_bar_image_size
        num_source_icons = (
            24  # This can be any number, it doesn't affect the bar's size
        )
        image_list = [
            pygame.Surface((icon_size, icon_size)) for _ in range(num_source_icons)
        ]

        active_bar = ActiveBar(position=(10, 20), image_list=image_list)

        # Check position
        assert active_bar.rect.topleft == (10, 20)

        # Check dimensions based on settings, not test-local variables
        expected_width = GFX.active_bar_image_size * GFX.active_bar_max_slots
        expected_height = GFX.active_bar_image_size
        assert active_bar.image.get_width() == expected_width
        assert active_bar.image.get_height() == expected_height

        pygame.quit()

    def test_add_and_remove_program(self, capsys):
        """Verify that programs can be added and removed from the bar."""
        pygame.init()
        icon_size = GFX.active_bar_image_size
        # Create a list of dummy icons with unique colors for easy identification
        image_list = [pygame.Surface((icon_size, icon_size)) for _ in range(10)]
        for i, img in enumerate(image_list):
            img.fill((i + 1, 0, 0))

        active_bar = ActiveBar(position=(0, 0), image_list=image_list)

        # Add a program and check that its icon is drawn in the first slot
        active_bar.add_program(program_id=3)
        assert 3 in active_bar.active_programs.values()
        assert active_bar.image.get_at((0, 0)) == image_list[3].get_at((0, 0))

        # Add a second program to the next slot
        active_bar.add_program(program_id=5)
        assert 5 in active_bar.active_programs.values()
        icon_pos_x = 1 * icon_size
        assert active_bar.image.get_at((icon_pos_x, 0)) == image_list[5].get_at((0, 0))

        # Remove the first program and check that its slot is cleared
        active_bar.remove_program(program_id=3)
        assert 3 not in active_bar.active_programs.values()
        assert active_bar.image.get_at((0, 0)) == UI_FACE

        # Fill the bar to capacity
        for i in range(GFX.active_bar_max_slots):
            if i not in active_bar.active_programs.values():
                active_bar.add_program(i)
        assert len(active_bar.active_programs) == GFX.active_bar_max_slots

        # Try to add one more program to a full bar to test warning
        active_bar.add_program(9)
        assert 9 not in active_bar.active_programs.values()
        captured = capsys.readouterr()
        assert "Warning: ActiveBar is full" in captured.out

        pygame.quit()

    def test_set_get_and_deactivate_by_slot(self):
        """Verify that programs can be set, retrieved, and deactivated by slot."""
        pygame.init()
        icon_size = GFX.active_bar_image_size
        image_list = [pygame.Surface((icon_size, icon_size)) for _ in range(10)]
        for i, img in enumerate(image_list):
            img.fill((i + 1, 0, 0))

        active_bar = ActiveBar(position=(0, 0), image_list=image_list)

        # Get from an empty slot
        assert active_bar.get_active_program(2) is None

        # Set a program in a specific slot
        active_bar.set_active_program(slot=2, program_id=7)
        assert active_bar.get_active_program(2) == 7

        # Check rendered image
        icon_pos_x = 2 * icon_size
        assert active_bar.image.get_at((icon_pos_x, 0)) == image_list[7].get_at((0, 0))

        # Deactivate the program from the slot
        active_bar.deactivate_program(slot=2)
        assert active_bar.get_active_program(2) is None
        assert active_bar.image.get_at((icon_pos_x, 0)) == UI_FACE

        # Deactivating an already empty slot should do nothing
        active_bar.deactivate_program(slot=2)
        assert active_bar.get_active_program(2) is None

        pygame.quit()

    def test_invalid_operations(self, capsys):
        """Verify warnings for invalid slot or program_id."""
        pygame.init()
        image_list = [
            pygame.Surface((GFX.active_bar_image_size, GFX.active_bar_image_size))
        ]
        active_bar = ActiveBar(position=(0, 0), image_list=image_list)

        # Test invalid operations and capture warnings
        active_bar.set_active_program(slot=99, program_id=0)
        assert "Invalid slot index 99" in capsys.readouterr().out
        active_bar.deactivate_program(slot=-1)
        assert "Invalid slot index -1" in capsys.readouterr().out
        active_bar.get_active_program(slot=100)
        assert "Invalid slot index 100" in capsys.readouterr().out
        active_bar.set_active_program(slot=0, program_id=99)
        assert "Invalid program_id 99" in capsys.readouterr().out

        pygame.quit()
