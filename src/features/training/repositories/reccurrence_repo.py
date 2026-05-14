from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.recurrence_rule import RecurrenceRule as RRDB
from src.features.training.domain.reccurence_rule import SessionRecurence as RREntity


class ReccurenceRepository(BaseRepository[RREntity, RRDB]):
    model = RRDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _to_domain(self, orm: RRDB) -> RREntity:
        return RREntity(
            id=orm.id,
            session_id=orm.session_id,
            jours=orm.days_week,
            weeks_interval=orm.week_interval,
            start_at=orm.start_at,
            end_at=orm.ends_at,
        )

    def _to_orm(self, entity: RREntity) -> RRDB:
        return RRDB(
            session_id=entity.session_id,
            days_week=entity.jours,
            start_at=entity.start_at,
            ends_at=entity.end_at,
            week_interval=entity.weeks_interval,
        )
