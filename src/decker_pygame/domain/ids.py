"""This module defines type aliases for all domain-specific IDs."""

import uuid
from typing import NewType

AggregateId = NewType("AggregateId", uuid.UUID)
AreaId = NewType("AreaId", uuid.UUID)
CharacterId = NewType("CharacterId", uuid.UUID)
DeckId = NewType("DeckId", uuid.UUID)
ContractId = NewType("ContractId", uuid.UUID)
IceId = NewType("IceId", uuid.UUID)
NodeId = NewType("NodeId", uuid.UUID)
PlayerId = NewType("PlayerId", uuid.UUID)
ProgramId = NewType("ProgramId", uuid.UUID)
SystemId = NewType("SystemId", uuid.UUID)
