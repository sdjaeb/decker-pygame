"""This module contains the concrete implementations of the game states."""

from typing import TYPE_CHECKING, Optional

import pygame

from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.application.dtos import (
    ContractSummaryDTO,
    IceDataViewDTO,
    ShopItemViewDTO,
)
from decker_pygame.domain.ids import ContractId
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.char_data_view import CharDataView
from decker_pygame.presentation.components.contract_data_view import ContractDataView
from decker_pygame.presentation.components.contract_list_view import ContractListView
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.ice_data_view import IceDataView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.matrix_run_view import MatrixRunView
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.shop_item_view import ShopItemView
from decker_pygame.presentation.components.shop_view import ShopView
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.states.game_states import BaseState

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.presentation.game import Game


class IntroState(BaseState):
    """The state for the game's introduction sequence."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> IntroView:
        """Factory function to create the IntroView."""
        return IntroView(on_continue=self.game._continue_from_intro)

    def on_enter(self) -> None:
        """Open the intro view when entering this state."""
        self.game.view_manager.toggle_view("intro_view", self._factory)

    def on_exit(self) -> None:
        """Close the intro view when exiting this state."""
        # Calling toggle_view on an existing view will close it.
        self.game.view_manager.toggle_view("intro_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)


class NewCharState(BaseState):
    """The state for creating a new character."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> NewCharView:
        """Factory function to create the NewCharView."""
        return NewCharView(on_create=self.game._handle_character_creation)

    def on_enter(self) -> None:
        """Open the new character view when entering this state."""
        self.game.view_manager.toggle_view("new_char_view", self._factory)

    def on_exit(self) -> None:
        """Close the new character view when exiting this state."""
        # Calling toggle_view on an existing view will close it.
        self.game.view_manager.toggle_view("new_char_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)


class HomeState(BaseState):
    """The main hub state of the game."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _on_increase_skill(self, skill_name: str) -> None:
        """Callback to handle increasing a skill."""

        def action() -> None:
            self.game.character_service.increase_skill(
                self.game.character_id, skill_name
            )

        self.game._execute_and_refresh_view(action, self._toggle_char_data_view)

    def _on_decrease_skill(self, skill_name: str) -> None:
        """Callback to handle decreasing a skill."""

        def action() -> None:
            self.game.character_service.decrease_skill(
                self.game.character_id, skill_name
            )

        self.game._execute_and_refresh_view(action, self._toggle_char_data_view)

    def _toggle_char_data_view(self) -> None:
        """Opens or closes the character data view."""

        def factory() -> Optional["CharDataView"]:
            view_data = self.game.character_service.get_character_view_data(
                self.game.character_id, self.game.player_id
            )
            if not view_data:
                self.game.show_message(
                    "Error: Could not retrieve character/player data."
                )
                return None
            return CharDataView(
                position=(150, 100),
                data=view_data,
                on_close=self._toggle_char_data_view,
                on_increase_skill=self._on_increase_skill,
                on_decrease_skill=self._on_decrease_skill,
            )

        self.game.view_manager.toggle_view("char_data_view", factory)

    def _toggle_deck_view(self) -> None:
        """Opens or closes the deck view."""

        def factory() -> Optional["DeckView"]:
            char_data = self.game.character_service.get_character_data(
                self.game.character_id
            )
            if not char_data:
                self.game.show_message(
                    "Error: Could not retrieve character data to find deck."
                )
                return None

            deck_data = self.game.deck_service.get_deck_view_data(char_data.deck_id)
            if not deck_data:
                self.game.show_message("Error: Could not retrieve deck data.")
                return None

            return DeckView(
                data=deck_data,
                on_close=self._toggle_deck_view,
                on_order=self._handle_order_click,
                on_program_click=self._on_program_click,
            )

        self.game.view_manager.toggle_view("deck_view", factory)

    def _toggle_order_view(self) -> None:
        """Opens or closes the deck ordering view."""

        def factory() -> Optional["OrderView"]:
            char_data = self.game.character_service.get_character_data(
                self.game.character_id
            )
            if not char_data:
                self.game.show_message(
                    "Error: Could not retrieve character data to find deck."
                )
                return None

            deck_data = self.game.deck_service.get_deck_view_data(char_data.deck_id)
            if not deck_data:
                self.game.show_message("Error: Could not retrieve deck data.")
                return None

            return OrderView(
                data=deck_data,
                on_close=self._handle_order_close,
                on_move_up=self._on_move_program_up,
                on_move_down=self._on_move_program_down,
            )

        self.game.view_manager.toggle_view("order_view", factory)

    def _handle_order_click(self) -> None:
        """Handles the transition from DeckView to OrderView."""
        self._toggle_deck_view()  # Close deck view
        self._toggle_order_view()  # Open order view

    def _handle_order_close(self) -> None:
        """Handles closing the OrderView and re-opening the DeckView."""
        self._toggle_order_view()
        self._toggle_deck_view()

    def _perform_move_up(self, program_name: str) -> None:
        """Helper to perform the domain logic for moving a program up."""
        char_data = self.game.character_service.get_character_data(
            self.game.character_id
        )
        if not char_data:
            raise Exception("Could not find character to modify deck.")
        self.game.deck_service.move_program_up(char_data.deck_id, program_name)

    def _on_move_program_up(self, program_name: str) -> None:
        """Callback to handle moving a program up in the deck order."""
        self.game._execute_and_refresh_view(
            lambda: self._perform_move_up(program_name), self._toggle_order_view
        )

    def _perform_move_down(self, program_name: str) -> None:
        """Helper to perform the domain logic for moving a program down."""
        char_data = self.game.character_service.get_character_data(
            self.game.character_id
        )
        if not char_data:
            raise Exception("Could not find character to modify deck.")
        self.game.deck_service.move_program_down(char_data.deck_id, program_name)

    def _on_move_program_down(self, program_name: str) -> None:
        """Callback to handle moving a program down in the deck order."""
        self.game._execute_and_refresh_view(
            lambda: self._perform_move_down(program_name), self._toggle_order_view
        )

    def _toggle_contract_list_view(self) -> None:
        """Opens or closes the contract list view."""

        def factory() -> Optional[ContractListView]:
            contracts = self.game.contract_service.get_available_contracts()
            if not contracts:
                self.game.show_message("No contracts available.")
                return None

            view = ContractListView(
                position=(200, 150),
                size=(450, 300),
                on_contract_selected=self._on_contract_selected,
            )
            view.set_contracts(contracts)
            return view

        self.game.view_manager.toggle_view("contract_list_view", factory)

    def _on_contract_selected(self, contract_dto: Optional[ContractSummaryDTO]) -> None:
        """Callback for when a contract is selected in the list."""

        def factory() -> Optional[ContractDataView]:
            # If a contract is selected, pass its details to the ContractDataView
            if contract_dto:
                return ContractDataView(
                    position=(200, 150),
                    size=(400, 300),
                    contract=contract_dto,
                    on_accept=self._on_accept_contract,
                )
            # Otherwise, return None to close the view if it's open
            return None  # This is intentional for closing the view

        self.game.view_manager.toggle_view("contract_data_view", factory)

    def _on_accept_contract(self, contract_id: ContractId) -> None:
        """Callback for when a contract is accepted."""
        self.game.logging_service.log("Contract Accepted", {"id": str(contract_id)})
        self.game.show_message(f"Contract {str(contract_id)[:8]}... accepted.")

    def _toggle_ice_data_view(self, data: Optional[IceDataViewDTO] = None) -> None:
        """Opens or closes the ICE data view."""

        def factory() -> Optional[IceDataView]:
            if data:
                return IceDataView(data=data, on_close=self._toggle_ice_data_view)
            return None

        self.game.view_manager.toggle_view("ice_data_view", factory)

    def _toggle_build_view(self) -> None:
        """Opens or closes the build view."""

        def factory() -> Optional[BuildView]:
            schematics = self.game.crafting_service.get_character_schematics(
                self.game.character_id
            )
            if not schematics:
                self.game.show_message("No schematics known.")
                return None
            return BuildView(
                position=(200, 150),
                size=(400, 300),
                schematics=schematics,
                on_build_click=self._handle_build_click,
            )

        self.game.view_manager.toggle_view("build_view", factory)

    def _handle_build_click(self, schematic_name: str) -> None:
        """Callback for when a build button is clicked in the BuildView."""
        try:
            self.game.crafting_service.craft_item(
                self.game.character_id, schematic_name
            )
        except CraftingError as e:
            self.game.show_message(f"Crafting failed: {e}")

    def _toggle_shop_view(self) -> None:
        """Opens or closes the shop view."""

        def factory() -> Optional[ShopView]:
            shop_data = self.game.shop_service.get_shop_view_data("DefaultShop")
            if not shop_data:
                self.game.show_message("Error: Could not load shop data.")
                return None
            return ShopView(
                data=shop_data,
                on_close=self._toggle_shop_view,
                on_purchase=self._on_purchase,
                on_view_details=self._on_show_item_details,
            )

        self.game.view_manager.toggle_view("shop_view", factory)

    def _toggle_shop_item_view(self, data: Optional["ShopItemViewDTO"] = None) -> None:
        """Opens or closes the Shop Item details view."""

        def factory() -> Optional["ShopItemView"]:
            if data:
                return ShopItemView(
                    data=data,
                    on_close=self._toggle_shop_item_view,
                )
            return None

        self.game.view_manager.toggle_view("shop_item_view", factory)

    def _perform_purchase(self, item_name: str) -> None:
        """Helper to perform the domain logic for purchasing an item."""
        # For now, we assume a single, default shop.
        self.game.shop_service.purchase_item(
            self.game.character_id, item_name, "DefaultShop"
        )
        self.game.show_message(f"Purchased {item_name}.")

    def _on_purchase(self, item_name: str) -> None:
        """Callback to handle purchasing an item from the shop."""
        self.game._execute_and_refresh_view(
            lambda: self._perform_purchase(item_name), self._toggle_shop_view
        )

    def _on_show_item_details(self, item_name: str) -> None:
        """Callback to handle displaying details for a specific shop item."""
        item_details = self.game.shop_service.get_item_details("DefaultShop", item_name)
        if item_details:
            self._toggle_shop_item_view(item_details)
        else:
            self.game.show_message(f"Could not retrieve details for {item_name}.")

    def _toggle_transfer_view(self) -> None:
        """Opens or closes the program transfer view."""

        def factory() -> Optional["TransferView"]:
            view_data = self.game.deck_service.get_transfer_view_data(
                self.game.character_id
            )
            if not view_data:
                self.game.show_message("Error: Could not retrieve transfer data.")
                return None
            return TransferView(
                data=view_data,
                on_close=self._toggle_transfer_view,
                on_move_to_deck=self._on_move_program_to_deck,
                on_move_to_storage=self._on_move_program_to_storage,
            )

        self.game.view_manager.toggle_view("transfer_view", factory)

    def _on_move_program_to_deck(self, program_name: str) -> None:
        """Callback to handle moving a program to the deck."""

        def action() -> None:
            self.game.deck_service.move_program_to_deck(
                self.game.character_id, program_name
            )

        self.game._execute_and_refresh_view(action, self._toggle_transfer_view)

    def _on_move_program_to_storage(self, program_name: str) -> None:
        """Callback to handle moving a program to storage."""

        def action() -> None:
            self.game.deck_service.move_program_to_storage(
                self.game.character_id, program_name
            )

        self.game._execute_and_refresh_view(action, self._toggle_transfer_view)

    def _factory(self) -> HomeView:
        """Factory function to create the HomeView."""
        return HomeView(
            on_char=self._toggle_char_data_view,
            on_deck=self._toggle_deck_view,
            on_contracts=self._toggle_contract_list_view,
            on_build=self._toggle_build_view,
            on_shop=self._toggle_shop_view,
            on_transfer=self._toggle_transfer_view,
            on_projects=self.game.toggle_project_data_view,
        )

    def on_enter(self) -> None:
        """Open the home view when entering this state."""
        self.game.view_manager.toggle_view("home_view", self._factory)

    def on_exit(self) -> None:
        """Close the home view when exiting this state."""
        self.game.view_manager.toggle_view("home_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)

    def _on_program_click(self, program_name: str) -> None:
        """Callback for when a program is clicked, to show its details."""
        ice_data = self.game.deck_service.get_ice_data(program_name)
        if not ice_data:
            self.game.show_message(f"No detailed data available for {program_name}.")
            return
        self._toggle_ice_data_view(ice_data)


class MatrixRunState(BaseState):
    """The state for an active matrix run."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def _factory(self) -> MatrixRunView:
        """Factory function to create the MatrixRunView."""
        return MatrixRunView(asset_service=self.game.asset_service)

    def on_enter(self) -> None:
        """Open the matrix run view when entering this state."""
        self.game.view_manager.toggle_view("matrix_run_view", self._factory)

    def on_exit(self) -> None:
        """Close the matrix run view when exiting this state."""
        self.game.view_manager.toggle_view("matrix_run_view", self._factory)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Events are handled by the global input handler."""

    def update(self, dt: float) -> None:
        """Update game logic by delegating to the main game object."""
        self.game.update_sprites(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state by delegating to the main game object."""
        self.game.all_sprites.draw(screen)
