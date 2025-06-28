import pygame
import pygame.sprite

from decker_pygame.settings import GFX, UI_FACE


class ActiveBar(pygame.sprite.Sprite):
    """
    Represents the active programs bar, showing icons for active software.
    Ported from ActiveBar.cpp and ActiveBar.h.
    """
    image: pygame.Surface
    rect: pygame.Rect
    _image_list: list[pygame.Surface]
    _active_slots: list[bool]
    _image_indices: list[int]

    def __init__(
        self, position: tuple[int, int], image_list: list[pygame.Surface]
    ) -> None:
        """
        Initializes the ActiveBar.

        Args:
            position: The (x, y) position of the top-left corner of the bar.
            image_list: A list of all possible program icon surfaces.
        """
        super().__init__()

        self.width = GFX.active_bar_image_size * GFX.active_bar_max_slots
        self.height = GFX.active_bar_image_size

        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect(topleft=position)

        self._image_list = image_list
        self._active_slots = [False] * GFX.active_bar_max_slots
        self._image_indices = [0] * GFX.active_bar_max_slots

        self.update()

    def set_active_program(
        self, slot: int, image_index: int, is_active: bool = True
    ) -> None:
        """Sets the state of an active program slot."""
        if 0 <= slot < GFX.active_bar_max_slots:
            self._active_slots[slot] = is_active
            self._image_indices[slot] = image_index
        else:
            print(f"Warning: Invalid slot index {slot} for ActiveBar.")

    def update(self) -> None:
        """
        Redraws the active bar surface based on the current state.
        This is the equivalent of OnPaint in the original C++ code.
        """
        self.image.fill(UI_FACE)

        for i in range(GFX.active_bar_max_slots):
            if self._active_slots[i]:
                icon = self._image_list[self._image_indices[i]]
                dest_rect = pygame.Rect(
                    i * GFX.active_bar_image_size,  # x position
                    0,  # y position
                    GFX.active_bar_image_size,  # width
                    GFX.active_bar_image_size,  # height
                )
                self.image.blit(icon, dest_rect)