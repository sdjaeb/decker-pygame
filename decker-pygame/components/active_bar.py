import pygame

# Constants from ActiveBar.h and ActiveBar.cpp
MAX_ACTIVE = 6
ACTIVE_IMAGE_SIZE = 16
WHITE = (255, 255, 255)


class ActiveBar(pygame.sprite.Sprite):
    """
    Represents the active programs bar, showing icons for active software.
    Ported from ActiveBar.cpp and ActiveBar.h.
    """

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

        self.width = ACTIVE_IMAGE_SIZE * MAX_ACTIVE
        self.height = ACTIVE_IMAGE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect(topleft=position)

        self._image_list = image_list
        self._active_slots = [False] * MAX_ACTIVE
        self._image_indices = [0] * MAX_ACTIVE

        self.update()

    def set_active_program(
        self, slot: int, image_index: int, is_active: bool = True
    ) -> None:
        """Sets the state of an active program slot."""
        if 0 <= slot < MAX_ACTIVE:
            self._active_slots[slot] = is_active
            self._image_indices[slot] = image_index
        else:
            print(f"Warning: Invalid slot index {slot} for ActiveBar.")

    def update(self) -> None:
        """
        Redraws the active bar surface based on the current state.
        This is the equivalent of OnPaint in the original C++ code.
        """
        self.image.fill(WHITE)

        for i in range(MAX_ACTIVE):
            if self._active_slots[i]:
                icon = self._image_list[self._image_indices[i]]
                dest_rect = pygame.Rect(i * ACTIVE_IMAGE_SIZE, 0, ACTIVE_IMAGE_SIZE, ACTIVE_IMAGE_SIZE)
                self.image.blit(icon, dest_rect)