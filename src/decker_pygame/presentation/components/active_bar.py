"""This module defines the ActiveBar component for the main game UI."""

import pygame
import pygame.sprite

from decker_pygame.settings import GFX, UI_FACE


class ActiveBar(pygame.sprite.Sprite):
    """Represents the active programs bar, showing icons for active software.

    Ported from ActiveBar.cpp and ActiveBar.h.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner of the
            bar.
        image_list (list[pygame.Surface]): A list of all possible program icon surfaces.

    Attributes:
        image (pygame.Surface): The surface that represents the active bar.
        rect (pygame.Rect): The rectangular area of the active bar.
        active_programs (dict[int, int]): A mapping of slot index to program ID.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _image_list: list[pygame.Surface]
    active_programs: dict[int, int]  # {slot_index: program_id}

    def __init__(
        self, position: tuple[int, int], image_list: list[pygame.Surface]
    ) -> None:
        super().__init__()

        self.width = GFX.active_bar_image_size * GFX.active_bar_max_slots
        self.height = GFX.active_bar_image_size

        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect(topleft=position)

        self._image_list = image_list
        self.active_programs = {}

        self.update()

    def add_program(self, program_id: int) -> None:
        """Adds a program to the first available slot."""
        if len(self.active_programs) >= GFX.active_bar_max_slots:
            print("Warning: ActiveBar is full. Cannot add program.")
            return

        for slot in range(GFX.active_bar_max_slots):
            if slot not in self.active_programs:
                self.active_programs[slot] = program_id
                self.update()
                return

    def remove_program(self, program_id: int) -> None:
        """Removes a program from the bar by its ID."""
        slot_to_remove = None
        for slot, prog_id in self.active_programs.items():
            if prog_id == program_id:
                slot_to_remove = slot
                break

        if slot_to_remove is not None:
            del self.active_programs[slot_to_remove]
            self.update()

    def set_active_program(self, slot: int, program_id: int) -> None:
        """Sets or replaces a program in a specific slot."""
        if not (0 <= slot < GFX.active_bar_max_slots):
            print(f"Warning: Invalid slot index {slot} for ActiveBar.")
            return
        if not (0 <= program_id < len(self._image_list)):
            print(f"Warning: Invalid program_id {program_id} for ActiveBar.")
            return

        self.active_programs[slot] = program_id
        self.update()

    def deactivate_program(self, slot: int) -> None:
        """Deactivates a program in a specific slot."""
        if not (0 <= slot < GFX.active_bar_max_slots):
            print(f"Warning: Invalid slot index {slot} for ActiveBar.")
            return

        if slot in self.active_programs:
            del self.active_programs[slot]
            self.update()

    def get_active_program(self, slot: int) -> int | None:
        """Gets the program ID from a specific slot.

        Args:
            slot (int): The slot index to query.

        Returns:
            int | None: The program_id if the slot is active, otherwise None.
        """
        if not (0 <= slot < GFX.active_bar_max_slots):
            print(f"Warning: Invalid slot index {slot} for ActiveBar.")
            return None
        return self.active_programs.get(slot)

    def update(self) -> None:
        """Redraws the active bar surface based on the current state.

        This is the equivalent of OnPaint in the original C++ code.
        """
        self.image.fill(UI_FACE)

        for slot, program_id in self.active_programs.items():
            icon = self._image_list[program_id]
            dest_rect = pygame.Rect(
                slot * GFX.active_bar_image_size,
                0,
                GFX.active_bar_image_size,
                GFX.active_bar_image_size,
            )
            self.image.blit(icon, dest_rect)
