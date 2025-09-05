"""This module contains the domain service for handling dice rolls."""

import random


class DiceService:
    """A service for performing dice rolls based on game rules."""

    def roll(self, num_dice: int, num_sides: int, modifier: int = 0) -> int:
        """Rolls a specified number of dice and adds a modifier.

        For example, a 3d6+2 roll would be roll(3, 6, 2).
        """
        return sum(random.randint(1, num_sides) for _ in range(num_dice)) + modifier
