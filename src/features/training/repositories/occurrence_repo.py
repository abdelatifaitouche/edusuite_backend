from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from src.db.repositories.base_repository import BaseRepository
from src.features.training.domain.session_occurrence import (
    SessionOccurence as SOccurrenceEntity,
)
from src.features.training.models.session_occurrence import (
    SessionOccurrence as SOccurrenceDB,
)


class OccurrenceRepository(BaseRepository[SOccurrenceEntity, SOccurrenceDB]):
    model = SOccurrenceDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _to_domain(self, orm: SOccurrenceDB) -> SOccurrenceEntity:
        return SOccurrenceEntity(
            session_id=orm.session_id,
            start_at=orm.start_at,
            end_at=orm.end_at,
            status=orm.status,
            id=orm.id,
            planned_date=orm.date,
            notes=orm.note,
        )

    def _to_orm(self, entity: SOccurrenceEntity) -> SOccurrenceDB:
        return SOccurrenceDB(
            session_id=entity.session_id,
            start_at=entity.start_at,
            end_at=entity.end_at,
            status=entity.status,
            date=entity.planned_date,
            note=entity.notes,
        )

    async def bulk_insert(self, data: list[SOccurrenceEntity]):
        db_models = [self._to_orm(entity) for entity in data]

        self.db.add_all(db_models)

        await self.db.flush()
