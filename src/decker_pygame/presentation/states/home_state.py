from typing import TYPE_CHECKING, Optional

import pygame

from decker_pygame.presentation.components.char_data_view import CharDataView
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.ice_data_view import IceDataView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.protocols import BaseState
from decker_pygame.presentation.states.shop_state import ShopState

if TYPE_CHECKING:
    from decker_pygame.application.dtos import (
        IceDataViewDTO,
    )
    from decker_pygame.presentation.game import Game
    from decker_pygame.presentation.view_manager import View


class HomeState(BaseState):
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.home_view: View = None
        self.char_data_view: View = None
        self.deck_view: View = None
        self.order_view: View = None
        self.ice_data_view: View = None
        self.contract_list_view: View = None
        self.contract_data_view: View = None
        self.build_view: View = None
        self.transfer_view: View = None
        self.project_data_view: View = None

    def _on_shop(self) -> None:
        """Callback to transition to the shop state."""
        self.game.set_state(ShopState(self.game))

    def _on_char(self) -> None:
        """Callback to open/close the character data view."""

        def factory() -> Optional[CharDataView]:
            char_data = self.game.character_service.get_char_data_view_data(
                self.game.character_id
            )
            if char_data:
                return CharDataView(data=char_data, on_close=self._on_char)
            self.game.show_message("Could not load character data.")
            return None

        self.char_data_view = self.game.view_manager.toggle_view(
            "char_data_view", factory, self.game
        )

    def _on_program_click(self, program_name: str) -> None:
        """Callback to show details for a specific program."""
        ice_data = self.game.deck_service.get_ice_data_view_data(program_name)
        if ice_data:
            self._toggle_ice_data_view(ice_data)
        else:
            self.game.show_message(f"Could not get data for {program_name}")

    def _toggle_ice_data_view(self, data: Optional["IceDataViewDTO"] = None) -> None:
        """Opens or closes the ICE details view."""

        def factory() -> Optional[IceDataView]:
            if data:
                return IceDataView(data=data, on_close=self._toggle_ice_data_view)
            return None

        self.ice_data_view = self.game.view_manager.toggle_view(
            "ice_data_view", factory, self.game
        )

    def _on_order_deck(self, new_order: list[str]) -> None:
        """Callback to save the new deck order."""
        self.game.deck_service.reorder_deck(self.game.character_id, new_order)
        # Close the order view
        self._toggle_order_view()
        # Refresh the deck view by toggling it off and on
        self._on_deck()
        self._on_deck()

    def _toggle_order_view(self) -> None:
        """Opens or closes the deck ordering view."""

        def factory() -> Optional[OrderView]:
            order_data = self.game.deck_service.get_order_view_data(
                self.game.character_id
            )
            if order_data:
                return OrderView(
                    data=order_data,
                    on_close=self._toggle_order_view,
                    on_save=self._on_order_deck,
                )
            self.game.show_message("Could not load deck order data.")
            return None

        self.order_view = self.game.view_manager.toggle_view(
            "order_view", factory, self.game
        )

    def _on_deck(self) -> None:
        """Callback to open/close the deck view."""

        def factory() -> Optional[DeckView]:
            deck_data = self.game.deck_service.get_deck_view_data(
                self.game.character_id
            )
            if deck_data:
                return DeckView(
                    data=deck_data,
                    on_close=self._on_deck,
                    on_order=self._toggle_order_view,
                    on_program_click=self._on_program_click,
                )
            self.game.show_message("Could not load deck data.")
            return None

        self.deck_view = self.game.view_manager.toggle_view(
            "deck_view", factory, self.game
        )

    def _on_view_contract(self, contract_id: "ContractId") -> None:
        """Callback to show details for a specific contract."""
        contract_data = self.game.contract_service.get_contract_data_view_data(
            contract_id
        )
        if contract_data:
            self._toggle_contract_data_view(contract_data)
        else:
            self.game.show_message(f"Could not get data for contract {contract_id}")

    def _toggle_contract_data_view(
        self, data: Optional["ContractDataViewDTO"] = None
    ) -> None:
        """Opens or closes the contract details view."""

        def factory() -> Optional[ContractDataView]:
            if data:
                return ContractDataView(
                    data=data, on_close=self._toggle_contract_data_view
                )
            return None

        self.contract_data_view = self.game.view_manager.toggle_view(
            "contract_data_view", factory, self.game
        )

    def _on_contracts(self) -> None:
        """Callback to open/close the contract list view."""

        def factory() -> Optional[ContractListView]:
            contract_list_data = self.game.contract_service.get_contract_list_view_data(
                self.game.character_id
            )
            if contract_list_data:
                return ContractListView(
                    data=contract_list_data,
                    on_close=self._on_contracts,
                    on_view_contract=self._on_view_contract,
                )
            self.game.show_message("Could not load contract list.")
            return None

        self.contract_list_view = self.game.view_manager.toggle_view(
            "contract_list_view", factory, self.game
        )

    def _on_build_program(self, schematic: "Schematic") -> None:
        """Callback to build a program from a schematic."""
        try:
            self.game.project_service.build_from_schematic(
                self.game.character_id, schematic
            )
            self.game.show_message(f"Successfully built {schematic.name}.")
            # Close and reopen the build view to refresh the list
            self._on_build()
            self._on_build()
        except Exception as e:
            self.game.show_message(f"Error building program: {e}")

    def _on_build(self) -> None:
        """Callback to open/close the build view."""

        def factory() -> Optional[BuildView]:
            build_data = self.game.project_service.get_build_view_data(
                self.game.character_id
            )
            if build_data:
                return BuildView(
                    data=build_data,
                    on_close=self._on_build,
                    on_build=self._on_build_program,
                )
            return None

        self.build_view = self.game.view_manager.toggle_view(
            "build_view", factory, self.game
        )

    def _on_transfer_funds(self, target_name: str, amount: int) -> None:
        """Callback to transfer funds to another character."""
        try:
            self.game.character_service.transfer_credits(
                self.game.character_id, target_name, amount
            )
            self.game.show_message(f"Successfully transferred {amount} credits.")
            # Close and reopen the transfer view to refresh data
            self._on_transfer()
            self._on_transfer()
        except Exception as e:
            self.game.show_message(f"Error transferring funds: {e}")

    def _on_transfer(self) -> None:
        """Callback to open/close the transfer view."""

        def factory() -> Optional[TransferView]:
            transfer_data = self.game.character_service.get_transfer_view_data(
                self.game.character_id
            )
            if transfer_data:
                return TransferView(
                    data=transfer_data,
                    on_close=self._on_transfer,
                    on_transfer=self._on_transfer_funds,
                )
            return None

        self.transfer_view = self.game.view_manager.toggle_view(
            "transfer_view", factory, self.game
        )

    def _on_work_project(self, work_unit: "WorkUnit") -> None:
        """Callback to work on the current project."""
        self.game.project_service.work_on_project(self.game.character_id, work_unit)
        # Close and reopen the project view to refresh data
        self._on_projects()
        self._on_projects()

    def _on_build_from_schematic(self, schematic: "Schematic") -> None:
        """Callback to build a program from a schematic."""
        try:
            self.game.project_service.build_from_schematic(
                self.game.character_id, schematic
            )
            self.game.show_message(f"Successfully built {schematic.name}.")
            # Close and reopen the project view to refresh data
            self._on_projects()
            self._on_projects()
        except Exception as e:
            self.game.show_message(f"Error building program: {e}")

    def _on_projects(self) -> None:
        """Callback to open/close the project data view."""

        def factory() -> Optional[ProjectDataView]:
            project_data = self.game.project_service.get_project_data_view_data(
                self.game.character_id
            )
            if project_data:
                return ProjectDataView(
                    data=project_data,
                    on_close=self._on_projects,
                    on_work=self._on_work_project,
                    on_build=self._on_build_from_schematic,
                    on_new=lambda: self.game.show_message(
                        "New project not implemented yet."
                    ),
                )
            return None

        self.project_data_view = self.game.view_manager.toggle_view(
            "project_data_view", factory, self.game
        )

    def enter(self) -> None:
        """Create and show the HomeView when entering the state."""

        def factory() -> HomeView:
            return HomeView(
                on_char=self._on_char,
                on_deck=self._on_deck,
                on_contracts=self._on_contracts,
                on_build=self._on_build,
                on_shop=self._on_shop,
                on_transfer=self._on_transfer,
                on_projects=self._on_projects,
            )

        self.home_view = self.game.view_manager.toggle_view(
            "home_view", factory, self.game
        )

    def exit(self) -> None:
        """Close all views managed by this state when exiting."""
        self.game.view_manager.toggle_view("home_view", None, self.game)
        self.game.view_manager.toggle_view("char_data_view", None, self.game)
        self.game.view_manager.toggle_view("deck_view", None, self.game)
        self.game.view_manager.toggle_view("order_view", None, self.game)
        self.game.view_manager.toggle_view("ice_data_view", None, self.game)
        self.game.view_manager.toggle_view("contract_list_view", None, self.game)
        self.game.view_manager.toggle_view("contract_data_view", None, self.game)
        self.game.view_manager.toggle_view("build_view", None, self.game)
        self.game.view_manager.toggle_view("transfer_view", None, self.game)
        self.game.view_manager.toggle_view("project_data_view", None, self.game)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.game.view_manager.handle_event(event)

    def update(self, dt: int, total_seconds: int) -> None:
        self.game.view_manager.update(dt, total_seconds)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.view_manager.draw(screen)

    def get_sprites(self) -> list[pygame.sprite.Sprite]:
        # Sprites are now managed by the ViewManager, so the state doesn't need to.
        return []
