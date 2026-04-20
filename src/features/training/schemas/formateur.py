from pydantic import BaseModel
from uuid import UUID


from src.features.training.enums.formateur_enums import FormateurStatus
from src.features.training.enums.formation_enums import DomainFormation


class FormateurRead(BaseModel):
    id: UUID
    nom: str
    prenom: str
    email: str | None = None
    telephone: str | None = None
    specialite: DomainFormation | None = None
    status: FormateurStatus

    model_config = {"from_attributes": True}


class FormateurCreate(BaseModel):
    nom: str
    prenom: str
    email: str | None = None
    telephone: str | None = None
    specialite: str | None = None
