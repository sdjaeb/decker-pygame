"""This module defines the PygameInputHandler for the presentation layer."""

from collections.abc import Callable
from typing import TYPE_CHECKING

import pygame

from decker_pygame.settings import DEV_SETTINGS

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.ports.service_interfaces import LoggingServiceInterface
    from decker_pygame.presentation.game import Game


class PygameInputHandler:
    """A dedicated Presentation Adapter for handling user input.

    Translates raw Pygame events into calls to the Game object.
    """

    _key_map: dict[int, Callable[[], None]]

    def __init__(self, game: "Game", logging_service: "LoggingServiceInterface"):
        self._game = game
        self._logging_service = logging_service
        self._key_map = {
            pygame.K_h: self._game.toggle_home_view,
            pygame.K_b: self._game.toggle_build_view,
            pygame.K_c: self._game.toggle_char_data_view,
            pygame.K_t: self._game.toggle_transfer_view,
            pygame.K_l: self._game.toggle_contract_list_view,
            pygame.K_d: self._game.toggle_contract_data_view,
            pygame.K_p: self._game.toggle_deck_view,
            pygame.K_f: lambda: self._game.show_file_access_view("corp_server_1"),
            pygame.K_e: lambda: self._game.toggle_entry_view("corp_server_1"),
            pygame.K_o: self._game.toggle_options_view,
            pygame.K_u: self._game.toggle_sound_edit_view,
            pygame.K_r: self._game.toggle_new_project_view,
            pygame.K_q: self._game.quit,
        }

    def handle_events(self) -> None:
        """Process the event queue and delegate to appropriate handlers."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.quit()
                return  # Exit early if quitting

            if event.type == pygame.KEYDOWN:
                if action := self._key_map.get(event.key):
                    action()

                if DEV_SETTINGS.enabled:
                    self._logging_service.log(
                        "Key Press", {"key": pygame.key.name(event.key)}
                    )

            # Delegate events to active views that need to handle mouse clicks, etc.
            for view in [
                self._game.intro_view,
                self._game.new_char_view,
                self._game.rest_view,
                self._game.mission_results_view,
                self._game.home_view,
                self._game.build_view,
                self._game.char_data_view,
                self._game.deck_view,
                self._game.transfer_view,
                self._game.shop_view,
                self._game.order_view,
                self._game.contract_list_view,
                self._game.contract_data_view,
                self._game.ice_data_view,
                self._game.file_access_view,
                self._game.entry_view,
                self._game.options_view,
                self._game.sound_edit_view,
                self._game.new_project_view,
            ]:
                if view:
                    view.handle_event(event)
