from dataclasses import dataclass
from uuid import UUID
from src.features.training.enums.salle import SalleState
from src.features.training.models.salle import Salle as SalleDB


@dataclass
class Salle:
    name: str
    size: int
    status: SalleState
    id: UUID | None = None

    @staticmethod
    def to_domaine(orm: SalleDB):
        return Salle(id=orm.id, name=orm.name, size=orm.size, status=orm.status)
