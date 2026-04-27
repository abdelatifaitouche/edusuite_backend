from pydantic import BaseModel
from src.features.training.enums.formation_enums import (
    TypeFormation,
    DomainFormation,
    StatusFormation,
    NiveauFormation,
)

from uuid import UUID


class ReadFormation(BaseModel):
    id: UUID
    titre: str
    code: str
    description: str
    domaine: DomainFormation | None = None
    type: TypeFormation | None = None
    niveau: NiveauFormation | None = None
    duree_jours: int
    heures_par_jour: int
    prix: float
    certifiante: bool
    status: StatusFormation | None = None

    model_config = {"from_attributes": True}


class CreateFormation(BaseModel):
    titre: str
    code: str
    description: str
    domaine: DomainFormation
    type: TypeFormation | None = None
    niveau: NiveauFormation | None = None
    duree_jours: int
    heures_par_jour: int
    prix: float
    certifiante: bool
    status: StatusFormation | None = None
