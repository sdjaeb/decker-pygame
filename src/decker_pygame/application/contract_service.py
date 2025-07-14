"""This module defines the application service for contract-related operations.

It includes the ContractService, which orchestrates use cases like retrieving
available contracts, and the Data Transfer Objects (DTOs) used to pass contract
data to the presentation layer.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.ids import ContractId
from decker_pygame.ports.repository_interfaces import ContractRepositoryInterface
from decker_pygame.ports.service_interfaces import ContractServiceInterface

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.domain.contract import Contract


@dataclass(frozen=True)
class ContractSummaryDTO:
    """A summary of a contract for list views."""

    # ContractId is a NewType of UUID, so it's fine to use it directly here.
    id: ContractId
    title: str
    client: str
    reward: int

    @classmethod
    def from_domain(cls, contract: "Contract") -> "ContractSummaryDTO":
        """Create a DTO from a Contract domain object."""
        return cls(
            # The domain object's ID is a generic AggregateId; cast it.
            id=ContractId(contract.id),
            title=contract.title,
            client=contract.client,
            reward=contract.reward_credits,
        )


class ContractService(ContractServiceInterface):
    """Application service for contract-related operations."""

    def __init__(
        self,
        contract_repo: ContractRepositoryInterface,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self.contract_repo = contract_repo
        self.event_dispatcher = event_dispatcher

    def get_available_contracts(self) -> list[ContractSummaryDTO]:
        """Retrieves a list of summaries for all available contracts."""
        contracts = self.contract_repo.get_all()
        return [ContractSummaryDTO.from_domain(c) for c in contracts]
