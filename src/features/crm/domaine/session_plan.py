from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from src.features.crm.enums.sessionplan_state import SessionPlanStatus, LocationType


@dataclass
class SessionPlan:
    expected_students: int
    location_type: LocationType
    venue_cost: float
    cost_per_student: float

    created_at: datetime | None = None
    updated_at: datetime | None = None

    id: UUID | None = None
    status: SessionPlanStatus | None = None
    opportunity_id: UUID | None = None
