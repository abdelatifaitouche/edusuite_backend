from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.features.crm.models.session_plan import SessionPlan as SessionPlanDB
from src.features.crm.domaine.session_plan import SessionPlan as SessionPlanEntity


class SessionPlanRepo(BaseRepository[SessionPlanEntity, SessionPlanDB]):
    model = SessionPlanDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

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
