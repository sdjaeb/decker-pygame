"""This module defines the ShopState for the game."""

from typing import TYPE_CHECKING, Optional

import pygame

from decker_pygame.application.dtos import ShopItemViewDTO
from decker_pygame.application.shop_service import ShopServiceError
from decker_pygame.presentation.components.shop_item_view import ShopItemView
from decker_pygame.presentation.components.shop_view import ShopView
from decker_pygame.presentation.protocols import BaseState
from decker_pygame.presentation.states.home_state import HomeState

if TYPE_CHECKING:
    from decker_pygame.presentation.game import Game
    from decker_pygame.presentation.view_manager import View


class ShopState(BaseState):
    """A game state for when the player is interacting with a shop."""

    def __init__(self, game: "Game"):
        self.game = game
        self.shop_view: View = None
        self.shop_item_view: View = None

    def _on_purchase(self, item_name: str) -> None:
        """Callback to handle purchasing an item from the shop."""
        try:
            # For now, we assume a single, default shop.
            self.game.shop_service.purchase_item(
                self.game.character_id, item_name, "DefaultShop"
            )
            self.game.show_message(f"Purchased {item_name}.")
            # Refresh the view by re-entering the state
            self.exit()
            self.enter()
        except ShopServiceError as e:
            self.game.show_message(f"Error: {e}")

    def _on_show_item_details(self, item_name: str) -> None:
        """Callback to show detailed info for a shop item."""
        item_details = self.game.shop_service.get_item_details("DefaultShop", item_name)
        if item_details:
            self._toggle_shop_item_view(item_details)
        else:
            self.game.show_message(f"Could not retrieve details for {item_name}.")

    def _toggle_shop_item_view(self, data: Optional["ShopItemViewDTO"] = None) -> None:
        """Opens or closes the Shop Item details view."""

        def factory() -> Optional["ShopItemView"]:
            if data:
                return ShopItemView(
                    data=data,
                    on_close=self._toggle_shop_item_view,
                )
            return None

        self.shop_item_view = self.game.view_manager.toggle_view(
            "shop_item_view", factory, self.game
        )

    def _on_close(self) -> None:
        """Callback to transition back to the home state."""
        self.game.set_state(HomeState(self.game))

    def enter(self) -> None:
        """Create and show the ShopView when entering the state."""

        def factory() -> Optional[ShopView]:
            shop_data = self.game.shop_service.get_shop_view_data("DefaultShop")
            if not shop_data:
                self.game.show_message("Error: Could not load shop data.")
                self._on_close()  # Transition back if shop can't be loaded
                return None
            return ShopView(
                data=shop_data,
                on_close=self._on_close,
                on_purchase=self._on_purchase,
                on_view_details=self._on_show_item_details,
            )

        self.shop_view = self.game.view_manager.toggle_view(
            "shop_view", factory, self.game
        )

    def exit(self) -> None:
        """Close all views managed by this state."""
        self.game.view_manager.toggle_view("shop_view", None, self.game)
        self.game.view_manager.toggle_view("shop_item_view", None, self.game)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.game.view_manager.handle_event(event)

    def update(self, dt: int, total_seconds: int) -> None:
        self.game.view_manager.update(dt, total_seconds)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.view_manager.draw(screen)

    def get_sprites(self) -> list[pygame.sprite.Sprite]:
        return []
