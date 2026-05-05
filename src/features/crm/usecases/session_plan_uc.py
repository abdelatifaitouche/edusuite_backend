from uuid import UUID
from typing import override
from src.db.usecases.base_usecase import BaseUC
from src.features.crm.repository.session_plan_repo import SessionPlanRepo
from src.features.crm.schemas.session_plan import (
    ReadSessionPlan,
    CreateSessionPlan,
    UpdateSessionPlan,
)
from src.features.crm.enums.sessionplan_state import SessionPlanStatus
from src.features.crm.domaine.session_plan import SessionPlan as SessionPlanEntity
from src.features.crm.repository.opportunity_repo import OpportunityRepo
from src.features.crm.enums.opportunity_states import OpportunityStates


class SessionPlanUC(BaseUC[SessionPlanEntity, CreateSessionPlan, UpdateSessionPlan]):
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

    async def _apply_update(
        self, entity: SessionPlanEntity, data: UpdateSessionPlan
    ) -> SessionPlanEntity:

        if entity.status == SessionPlanStatus.LOCKED:
            raise Exception("locked")

        if data.cost_per_student:
            entity.cost_per_student = data.cost_per_student

        if data.venue_cost:
            entity.venue_cost = data.venue_cost

        if data.expected_students:
            entity.expected_students = data.expected_students

        return entity

    async def submit_session_plan(self, entity_id: UUID):
        entity = await self.get_by_id(entity_id)

        if entity.status != SessionPlanStatus.DRAFT:
            raise Exception("Cannot approve a non draft")

        entity.status = SessionPlanStatus.SUBMITED

        return await self.repo.save(entity)

    async def approve_session_plan(self, entity_id: UUID):
        entity = await self.get_by_id(entity_id)

        if entity.status != SessionPlanStatus.SUBMITED:
            raise Exception("Session Not Submited")

        entity.status = SessionPlanStatus.APPROVED

        from src.features.crm.usecases.OpportunityUC import OpportunityUC
        from src.features.crm.repository.opportunity_repo import OpportunityRepo

        op_repo = OpportunityRepo(self.repo.db)
        op_uc = OpportunityUC(op_repo)

        if entity.opportunity_id:
            op = await op_uc.transition(entity.opportunity_id)

        return await self.repo.save(entity)

    async def create_session_plan(
        self, opportunity_id: str, data: CreateSessionPlan
    ) -> SessionPlanEntity:
        op_repo = OpportunityRepo(self.repo.db)

        op = await op_repo.get_by_id(UUID(opportunity_id))

        if op is None:
            raise Exception("Cannot find op")

        if op.status != OpportunityStates.NEED_ANALYSIS:
            raise Exception("Invalid States")

        if op.session_plan_id:
            raise Exception("Opporunity has session plan")

        if data.expected_students <= 0:
            raise Exception("Invalid number of students")

        if data.cost_per_student <= 0:
            raise Exception("Invalid Cost")
        entity: SessionPlanEntity = SessionPlanEntity(
            expected_students=data.expected_students,
            location_type=data.location_type,
            opportunity_id=UUID(opportunity_id),
            venue_cost=data.venue_cost,
            cost_per_student=data.cost_per_student,
        )
        return await self.repo.save(entity)

    async def get_session_plan(self, opportunity_id: str) -> SessionPlanEntity:

        session = await self.repo.get_by_opportunity_id(UUID(opportunity_id))

        if not session:
            raise Exception("No sesssion for this op")

        return session
