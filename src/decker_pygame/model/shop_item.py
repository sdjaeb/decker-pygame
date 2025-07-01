"""
Pydantic model for an item available in a Shop.
"""

from pydantic import BaseModel, Field

from decker_pygame.model.program import Program


class ShopItem(BaseModel):
    """Represents an item for sale, linking an item model to its stock."""

    # This can be expanded with Union[Program, Hardware, ...] later.
    item: Program
    stock: int = Field(
        ..., ge=0, description="How many units are available for purchase."
    )
