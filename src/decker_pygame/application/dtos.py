"""This module defines Data Transfer Objects (DTOs) for the application layer."""

from dataclasses import dataclass


@dataclass
class MissionResultsDTO:
    """Data for displaying the results of a mission."""

    contract_name: str
    was_successful: bool
    credits_earned: int
    reputation_change: int


@dataclass
class RestViewData:
    """Data for displaying the rest view."""

    cost: int
    health_recovered: int
