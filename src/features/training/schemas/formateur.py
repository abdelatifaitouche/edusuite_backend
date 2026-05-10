from pydantic import BaseModel
from uuid import UUID


from src.features.training.enums.formateur_enums import FormateurStatus
from src.features.training.enums.formation_enums import DomainFormation


class ReadMiniCourse(BaseModel):
    id: UUID
    titre: str

    model_config = {"from_attributes": True}


class FormateurSummary(BaseModel):
    id: UUID
    nom: str
    prenom: str
    email: str
    telephone: str
    status: FormateurStatus
    specialite: DomainFormation

    model_config = {"from_attributes": True}


class FormateurRead(BaseModel):
    id: UUID
    nom: str
    prenom: str
    email: str | None = None
    telephone: str | None = None
    specialite: DomainFormation | None = None
    daily_rate: float | None = 0.0
    year_of_experience: int | None = 0
    ville: str | None = "Unkown"
    status: FormateurStatus
    courses: list[ReadMiniCourse] | None = None
    model_config = {"from_attributes": True}


class FormateurCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    telephone: str
    specialite: str
    year_of_experience: int | None = None
    ville: str | None = None
    daily_rate: float | None = None


class FormateurUpdate(BaseModel):
    daily_rate: float | None = None
    ville: str | None = None
    year_of_experience: int | None = None
