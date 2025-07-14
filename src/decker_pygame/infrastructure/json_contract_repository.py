"""A JSON file-based implementation of the Contract repository interface."""

import json
import os
from typing import Any

from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import ContractId
from decker_pygame.ports.repository_interfaces import ContractRepositoryInterface


class JsonFileContractRepository(ContractRepositoryInterface):
    """A repository that stores contract data in JSON files.

    Args:
        base_path (str): Directory where contract files are stored.
    """

    def __init__(self, base_path: str) -> None:
        self._base_path = base_path
        os.makedirs(self._base_path, exist_ok=True)

    def get_all(self) -> list[Contract]:
        """Retrieves all contracts from the repository."""
        contracts: list[Contract] = []
        if not os.path.exists(self._base_path):
            return contracts

        for filename in os.listdir(self._base_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self._base_path, filename)
                try:
                    with open(filepath) as f:
                        data: dict[str, Any] = json.load(f)
                        contracts.append(Contract.from_dict(data))
                except (json.JSONDecodeError, KeyError):
                    # Skip corrupted or invalid files
                    continue
        return contracts

    def _get_path(self, contract_id: ContractId) -> str:
        return os.path.join(self._base_path, f"{contract_id}.json")

    def get(self, contract_id: ContractId) -> Contract | None:
        """Retrieve a Contract aggregate from a JSON file, or None if not found."""
        filepath = self._get_path(contract_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath) as f:
            data = json.load(f)
        return Contract.from_dict(data)

    def save(self, contract: Contract) -> None:
        """Save a Contract aggregate to a JSON file."""
        filepath = self._get_path(ContractId(contract.id))
        with open(filepath, "w") as f:
            json.dump(contract.to_dict(), f, indent=4)
