from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.repositories.base_repository import BaseRepository
from src.features.crm.models.session_plan import SessionPlan as SessionPlanDB
from src.features.crm.domaine.session_plan import SessionPlan as SessionPlanEntity


class SessionPlanRepo(BaseRepository[SessionPlanEntity, SessionPlanDB]):
    model = SessionPlanDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_opportunity_id(
        self, opportunity_id: UUID
    ) -> SessionPlanEntity | None:
        stmt = select(self.model).where(self.model.opportunity_id == opportunity_id)

        result = await self.db.execute(stmt)

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    async def _orm_update(
        self, orm: SessionPlanDB, entity: SessionPlanEntity
    ) -> SessionPlanDB:

        if entity.status:
            orm.status = entity.status

        if entity.cost_per_student:
            orm.cost_per_student = entity.cost_per_student

        if entity.venue_cost:
            orm.venue_cost = entity.venue_cost

        if entity.expected_students:
            orm.expected_students = entity.expected_students
        return orm

    def _to_domain(self, orm: SessionPlanDB) -> SessionPlanEntity:
        return SessionPlanEntity(
            id=orm.id,
            opportunity_id=orm.opportunity_id,
            status=orm.status,
            venue_cost=orm.venue_cost,
            expected_students=orm.expected_students,
            location_type=orm.location_type,
            cost_per_student=orm.cost_per_student,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def _to_orm(self, entity: SessionPlanEntity) -> SessionPlanDB:
        return SessionPlanDB(
            id=entity.id,
            status=entity.status,
            venue_cost=entity.venue_cost,
            location_type=entity.location_type,
            cost_per_student=entity.cost_per_student,
            expected_students=entity.expected_students,
            opportunity_id=entity.opportunity_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
