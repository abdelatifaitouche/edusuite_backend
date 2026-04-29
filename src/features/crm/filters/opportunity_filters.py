from pydantic import BaseModel
from src.features.crm.enums.opportunity_states import OpportunityStates


class OpportunityFilters(BaseModel):
    status: OpportunityStates | None = None
