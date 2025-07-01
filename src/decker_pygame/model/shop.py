"""
Pydantic model for a Shop.
"""

from pydantic import BaseModel, Field

from decker_pygame.model.shop_item import ShopItem


class Shop(BaseModel):
    """Represents an in-game shop where items can be purchased."""

    name: str
    location: str  # Could link to an Area model later
    inventory: list[ShopItem] = Field(default_factory=list)
