from uuid import UUID
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from src.features.crm.enums.opportunity_states import OpportunityStates
from src.features.crm.domaine.session_plan import SessionPlan


@dataclass
class Opportunity:
    title: str
    status: OpportunityStates
    estimated_value: float
    probability: float
    expected_close_date: date

    session_plan_id: UUID | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    id: UUID | None = None
