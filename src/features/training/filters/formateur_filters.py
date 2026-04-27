from pydantic import BaseModel
from src.features.training.enums.formateur_enums import FormateurStatus


class FormateurFilters(BaseModel):
    status: FormateurStatus | None = None
