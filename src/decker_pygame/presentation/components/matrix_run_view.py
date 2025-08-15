"""This module defines the MatrixRunView, the main interface for hacking."""

import pygame

from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.components.alarm_bar import AlarmBar
from decker_pygame.presentation.components.health_bar import HealthBar
from decker_pygame.presentation.components.map_view import MapView
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.components.node_grid_view import NodeGridView
from decker_pygame.presentation.components.software_list_view import SoftwareListView
from decker_pygame.settings import RED, UI_FACE


class MatrixRunView(pygame.sprite.Sprite):
    """A composite view for the main matrix run/hacking interface.

    This view contains all the necessary HUD elements for a matrix run, such as
    the health bar, alarm level, and active programs.

    Args:
        asset_service (AssetService): The service for loading game assets.

    Attributes:
        image (pygame.Surface): The surface that represents this view.
        rect (pygame.Rect): The rectangular area of the view.
        components (pygame.sprite.Group[pygame.sprite.Sprite]): A group containing
            all the child HUD elements.
        node_grid_view (NodeGridView): The view for the matrix grid.
        map_view (MapView): The view for the system map.
        message_view (MessageView): The view for displaying text messages.
        software_list_view (SoftwareListView): The view for displaying loaded software.
        alarm_bar (AlarmBar): The view for the system alarm level.
        deck_health_bar (HealthBar): The player's deck health.
        mental_health_bar (HealthBar): The player's mental health.
        physical_health_bar (HealthBar): The player's physical health.
        shield_status_bar (HealthBar): The player's active shield status.
        transfer_progress_bar (HealthBar): The progress of a file transfer.
        trace_progress_bar (HealthBar): The progress of a system trace.
        ice_health_bar (HealthBar): The health of the targeted ICE.

    Raises:
        ValueError: If the required 'matrix_main' background image is not found
            in the provided AssetService.
    """

    _background: pygame.Surface | None = None

    image: pygame.Surface
    rect: pygame.Rect
    components: pygame.sprite.Group[pygame.sprite.Sprite]
    node_grid_view: NodeGridView
    map_view: MapView
    message_view: MessageView
    software_list_view: SoftwareListView
    alarm_bar: AlarmBar
    deck_health_bar: HealthBar
    mental_health_bar: HealthBar
    physical_health_bar: HealthBar
    shield_status_bar: HealthBar
    transfer_progress_bar: HealthBar
    trace_progress_bar: HealthBar
    ice_health_bar: HealthBar

    def __init__(self, asset_service: AssetService):
        super().__init__()

        if MatrixRunView._background is None:
            background_surface = asset_service.get_image("matrix_main")
            if background_surface is None:
                raise ValueError(
                    "MatrixRunView background 'matrix_main' not found in assets."
                )
            MatrixRunView._background = background_surface

        self.image = MatrixRunView._background.copy()
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.components = pygame.sprite.Group[pygame.sprite.Sprite]()

        self.node_grid_view = NodeGridView(position=(194, 49), size=(240, 240))
        self.components.add(self.node_grid_view)

        # TODO: Replace with real data from a service
        dummy_nodes = {"cpu": (50, 50), "data_store_1": (100, 100)}
        dummy_connections = [("cpu", "data_store_1")]
        self.map_view = MapView(
            position=(451, 12),
            size=(177, 166),
            nodes=dummy_nodes,
            connections=dummy_connections,
        )
        pygame.draw.rect(self.map_view.image, RED, self.map_view.image.get_rect(), 3)
        self.components.add(self.map_view)

        self.message_view = MessageView(
            position=(194, 367), size=(434, 101), background_color=UI_FACE
        )
        self.message_view.set_text("Welcome to the Matrix.")
        pygame.draw.rect(
            self.message_view.image, RED, self.message_view.image.get_rect(), 3
        )
        self.components.add(self.message_view)

        self.software_list_view = SoftwareListView(position=(12, 42), size=(165, 399))
        self.components.add(self.software_list_view)

        self.alarm_bar = AlarmBar(position=(206, 342), width=84, height=8)
        self.components.add(self.alarm_bar)

        self.deck_health_bar = HealthBar(position=(548, 195), width=80, height=8)
        self.mental_health_bar = HealthBar(position=(548, 220), width=80, height=8)
        self.physical_health_bar = HealthBar(position=(548, 234), width=80, height=8)
        self.shield_status_bar = HealthBar(position=(548, 259), width=80, height=8)
        self.transfer_progress_bar = HealthBar(position=(548, 284), width=80, height=8)
        self.trace_progress_bar = HealthBar(position=(548, 309), width=80, height=8)
        self.ice_health_bar = HealthBar(position=(354, 342), width=84, height=8)

        self.components.add(
            self.deck_health_bar,
            self.mental_health_bar,
            self.physical_health_bar,
            self.shield_status_bar,
            self.transfer_progress_bar,
            self.trace_progress_bar,
            self.ice_health_bar,
        )

    def update(self) -> None:
        """Update all components and redraw them on this view's surface."""
        assert self._background is not None, (
            "MatrixRunView background has not been loaded."
        )
        self.components.update()
        self.image.blit(self._background, (0, 0))
        self.components.draw(self.image)
