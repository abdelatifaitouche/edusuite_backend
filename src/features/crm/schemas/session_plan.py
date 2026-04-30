from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from src.features.crm.enums.sessionplan_state import SessionPlanStatus, LocationType


class ReadSessionPlan(BaseModel):
    id: UUID
    opportunity_id: UUID
    status: SessionPlanStatus
    expected_students: int
    location_type: LocationType
    venue_cost: float
    cost_per_student: float

    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class CreateSessionPlan(BaseModel):
    status: SessionPlanStatus = SessionPlanStatus.DRAFT
    expected_students: int
    location_type: LocationType
    venue_cost: float
    cost_per_student: float
    opportunity_id: UUID | None = None
