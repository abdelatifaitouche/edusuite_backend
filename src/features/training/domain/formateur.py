from dataclasses import dataclass
from uuid import UUID
from src.features.training.enums.formateur_enums import FormateurStatus


@dataclass
class BaseFormateur:
    nom: str
    prenom: str
    email: str
    telephone: str


@dataclass
class Formateur:
    prenom: str
    nom: str
    email: str
    daily_rate: float | None = None
    ville: str | None = None
    year_of_experience: int | None = None
    telephone: str | None = None
    specialite: str | None = None
    niveau_expertise: str | None = None
    bio: str | None = None
    status: FormateurStatus | None = None
    cv_url: str | None = None

    id: UUID | None = None
