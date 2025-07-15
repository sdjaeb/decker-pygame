"""This module defines the application service for shop-related operations."""

import uuid
from typing import Optional, TypedDict

from decker_pygame.application.dtos import ShopItemDTO, ShopViewDTO
from decker_pygame.domain.ids import CharacterId, ProgramId
from decker_pygame.domain.program import Program
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import ShopServiceInterface


class ShopInventoryData(TypedDict):
    """Defines the structure for a shop's inventory data."""

    name: str
    items: list[ShopItemDTO]


# For now, we'll use a hardcoded inventory. In the future, this would come
# from a Shop aggregate and repository.
SHOP_INVENTORY: dict[str, ShopInventoryData] = {
    "DefaultShop": {
        "name": "The Digital Dive",
        "items": [
            ShopItemDTO(
                name="IcePick v1", cost=500, description="A basic intrusion program."
            ),
            ShopItemDTO(
                name="Hammer v1",
                cost=1200,
                description="A heavy-duty breaker program.",
            ),
        ],
    }
}


class ShopServiceError(Exception):
    """Base exception for shop service errors."""


class ShopService(ShopServiceInterface):
    """Application service for shop-related operations."""

    def __init__(self, character_repo: CharacterRepositoryInterface) -> None:
        self.character_repo = character_repo

    def get_shop_view_data(self, shop_id: str) -> Optional[ShopViewDTO]:
        """Retrieves the data needed to display a shop's inventory."""
        shop_data = SHOP_INVENTORY.get(shop_id)
        if not shop_data:
            return None
        return ShopViewDTO(shop_name=shop_data["name"], items=shop_data["items"])

    def purchase_item(
        self, character_id: CharacterId, item_name: str, shop_id: str
    ) -> None:
        """Orchestrates the use case of a character purchasing an item."""
        character = self.character_repo.get(character_id)
        if not character:
            raise ShopServiceError("Character not found.")

        shop_data = SHOP_INVENTORY.get(shop_id)
        if not shop_data:
            raise ShopServiceError("Shop not found.")

        try:
            item_to_buy = next(
                item for item in shop_data["items"] if item.name == item_name
            )
        except StopIteration:
            raise ShopServiceError(f"Item '{item_name}' not found in shop.") from None

        if character.credits < item_to_buy.cost:
            raise ShopServiceError("Insufficient credits.")

        character.credits -= item_to_buy.cost

        # This is a simplification. A real implementation would have more item details.
        new_program = Program(
            id=ProgramId(uuid.uuid4()), name=item_to_buy.name, size=10
        )
        character.stored_programs.append(new_program)

        self.character_repo.save(character)
        # In the future, we could emit an ItemPurchased event here.
