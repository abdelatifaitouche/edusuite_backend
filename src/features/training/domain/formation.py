from src.features.training.enums.formation_enums import (
    TypeFormation,
    StatusFormation,
    NiveauFormation,
    DomainFormation,
)

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Formation:
    titre: str
    code: str
    duree_jours: int
    heures_par_jour: int
    certifiante: bool

    domaine: DomainFormation
    id: UUID | None = None
    prix: float | None = None
    description: str | None = None
    type: TypeFormation | None = None
    niveau: NiveauFormation | None = None
    status: StatusFormation | None = None
