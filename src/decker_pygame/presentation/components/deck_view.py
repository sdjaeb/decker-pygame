import pygame


class DeckView(pygame.sprite.Sprite):
    """A UI component that displays the player's deck of programs."""

    def __init__(self) -> None:
        super().__init__()
