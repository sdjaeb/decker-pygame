from unittest.mock import Mock

import pygame


class _FakeView(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

    def handle_event(self, event):
        return None


def test_view_manager_toggle_adds_and_removes_modal():
    pygame.init()
    try:
        from decker_pygame.presentation.game import Game
        from decker_pygame.presentation.view_manager import ViewManager

        # Use a mock with a spec to satisfy type checkers
        game = Mock(spec=Game)
        game.all_sprites = pygame.sprite.Group()
        game.some_view = None
        vm = ViewManager(game=game)

        # Define a factory that returns a new FakeView
        def factory():
            return _FakeView()

        # Toggle open
        vm.toggle_view("some_view", factory)
        assert game.some_view is not None
        assert len(vm.modal_stack) == 1

        # Toggle close
        vm.toggle_view("some_view", factory)
        assert game.some_view is None
        assert len(vm.modal_stack) == 0
    finally:
        pygame.quit()
