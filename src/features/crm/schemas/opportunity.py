from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from src.features.crm.enums.opportunity_states import OpportunityStates
from src.features.crm.schemas.session_plan import ReadSessionPlan


class CreateOpportunity(BaseModel):
    title: str
    probability: float
    estimated_value: float
    expected_close_date: date
    status: OpportunityStates = OpportunityStates.NEW


class ReadOpporunity(BaseModel):
    id: UUID
    title: str
    probability: float
    estimated_value: float
    expected_close_date: date
    status: OpportunityStates
    session_plan: ReadSessionPlan | None = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class UpdateOpportunity(BaseModel):
    status: OpportunityStates | None = None
