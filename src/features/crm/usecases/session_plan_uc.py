from uuid import UUID
from typing import override
from src.db.usecases.base_usecase import BaseUC
from src.features.crm.repository.session_plan_repo import SessionPlanRepo
from src.features.crm.schemas.session_plan import ReadSessionPlan, CreateSessionPlan
from src.features.crm.domaine.session_plan import SessionPlan as SessionPlanEntity
from src.features.crm.repository.opportunity_repo import OpportunityRepo
from src.features.crm.enums.opportunity_states import OpportunityStates


class SessionPlanUC(BaseUC[SessionPlanEntity, CreateSessionPlan, ReadSessionPlan]):
    def __init__(self, repo: SessionPlanRepo):
        super().__init__(repo)
        self.repo: SessionPlanRepo = repo

    def _to_entity(self, data: CreateSessionPlan) -> SessionPlanEntity:
        return SessionPlanEntity(
            expected_students=data.expected_students,
            cost_per_student=data.cost_per_student,
            opportunity_id=data.opportunity_id,
            location_type=data.location_type,
            venue_cost=data.venue_cost,
        )

    async def create_session_plan(
        self, opportunity_id: str, data: CreateSessionPlan
    ) -> SessionPlanEntity:
        op_repo = OpportunityRepo(self.repo.db)

        op = await op_repo.get_by_id(UUID(opportunity_id))

        if op is None:
            raise Exception("Cannot find op")

        if op.status != OpportunityStates.NEED_ANALYSIS:
            raise Exception("Invalid States")

        if op.session_plan:
            raise Exception("Opporunity has session plan")

        if data.expected_students <= 0:
            raise Exception("Invalid number of students")

        if data.cost_per_student <= 0:
            raise Exception("Invalid Cost")
        entity: SessionPlanEntity = self._to_entity(data)
        return await self.repo.save(entity)
