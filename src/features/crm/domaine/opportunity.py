from uuid import UUID
from dataclasses import dataclass
from datetime import date, datetime
from src.features.crm.enums.opportunity_states import OpportunityStates


@dataclass
class Opportunity:
    title: str
    status: OpportunityStates
    estimated_value: float
    probability: float
    expected_close_date: date
    created_at: datetime | None = None
    updated_at: datetime | None = None
    id: UUID | None = None
