from pydantic import BaseModel


class FormationFilters(BaseModel):
    status: str | None = None
