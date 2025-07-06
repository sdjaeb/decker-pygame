from dataclasses import dataclass

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.contract_repository_interface import (
    ContractRepositoryInterface,
)
from decker_pygame.domain.ids import ContractId


@dataclass(frozen=True)
class ContractSummaryDTO:
    """A summary of a contract for list views."""

    # ContractId is a NewType of UUID, so it's fine to use it directly here.
    id: ContractId
    title: str
    client: str
    reward: int


class ContractService:
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
        return [
            ContractSummaryDTO(
                # Cast the AggregateId from the base class to the specific ContractId
                id=ContractId(c.id),
                title=c.title,
                client=c.client,
                reward=c.reward_credits,
            )
            for c in contracts
        ]
