from pydantic import BaseModel
from src.features.training.enums.formateur_enums import FormateurStatus
from src.features.training.enums.formation_enums import DomainFormation


class FormateurFilters(BaseModel):
    status: FormateurStatus | None = None
    specialite: DomainFormation | None = None
