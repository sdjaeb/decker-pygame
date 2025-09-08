"""This module defines the application service for contract-related operations.

It includes the ContractService, which orchestrates use cases like retrieving
available contracts.
"""

from decker_pygame.application.dtos import ContractSummaryDTO
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.ids import CharacterId, ContractId
from decker_pygame.ports.repository_interfaces import ContractRepositoryInterface
from decker_pygame.ports.service_interfaces import ContractServiceInterface


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

    def accept_contract(
        self, character_id: CharacterId, contract_id: ContractId
    ) -> None:
        """Marks a contract as accepted by a character."""
        # This is a placeholder implementation.
        # In the future, this would update the state of the contract and character.
        pass
