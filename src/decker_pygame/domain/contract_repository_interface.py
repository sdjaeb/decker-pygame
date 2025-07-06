from abc import ABC, abstractmethod

from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import ContractId


class ContractRepositoryInterface(ABC):
    """Interface for a repository that manages Contract aggregates."""

    @abstractmethod
    def get(self, contract_id: ContractId) -> Contract | None:
        """Retrieves a contract by its ID."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def save(self, contract: "Contract") -> None:
        """Saves a contract."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[Contract]:
        """Retrieves all available contracts."""
        raise NotImplementedError  # pragma: no cover
