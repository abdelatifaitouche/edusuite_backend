from pydantic import BaseModel, field_validator
from datetime import date
from src.features.training.enums.session import SessionOccurenceState


class OccurrenceFilters(BaseModel):
    status: SessionOccurenceState | None = None
    start_date: date | None = None
    end_date: date | None = None

    @field_validator("start_date", mode="before")
    @classmethod
    def default_start(cls, v):
        if v is None:
            today = date.today()
            return today.replace(day=1)
        return v

    @field_validator("end_date", mode="before")
    @classmethod
    def default_end(cls, v):

        if v is None:
            today = date.today()

            if today.month == 12:
                return today.replace(year=today.year + 1, month=1, day=1)

            return today.replace(month=today.month + 1, day=1)

        return v
