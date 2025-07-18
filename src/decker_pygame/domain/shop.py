"""This module defines domain models related to Shops."""

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from decker_pygame.domain.ids import ShopId, ShopItemId


class ShopItemType(Enum):
    """Enumeration for the different types of shop items."""

    PROGRAM = "Program"
    HARDWARE = "Hardware"
    BATTERY = "Battery"
    OTHER = "Other"


@dataclass
class ShopItem:
    """Represents an item available for sale in a shop."""

    # Required fields first
    name: str
    cost: int
    item_type: ShopItemType

    # Optional fields with defaults
    description: str = ""
    # This will hold data needed to create the actual item, e.g., program stats.
    data: dict[str, Any] = field(default_factory=dict)
    id: ShopItemId = field(default_factory=lambda: ShopItemId(uuid.uuid4()))


@dataclass
class Shop:
    """Represents a shop aggregate root."""

    # Required fields first
    name: str

    # Optional fields with defaults
    items: list[ShopItem] = field(default_factory=list)
    id: ShopId = field(default_factory=lambda: ShopId(uuid.uuid4()))
