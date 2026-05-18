from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from uuid import UUID
from sqlalchemy import insert, text, bindparam
from src.db.repositories.base_repository import BaseRepository
from src.features.training.domain.session_occurrence import (
    SessionOccurence as SOccurrenceEntity,
    ConflictResult,
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

    async def check_conflicts(
        self, expected_dates: list[date], formateur_id: UUID, salle_id: UUID
    ) -> ConflictResult | None:

        query = text(""" SELECT formateur_id,salle_id,o.date FROM sessions 
                     JOIN sessions_occurrences as o ON o.session_id=sessions.id
                     WHERE o.date IN :dates
                     AND (formateur_id = :formateur_id OR salle_id = :salle_id)""").bindparams(
            bindparam("dates", expanding=True),
        )

        result = await self.db.execute(
            query,
            {
                "dates": tuple(expected_dates),
                "formateur_id": formateur_id,
                "salle_id": salle_id,
            },
        )

        data = result.fetchall()

        if not data:
            return None

        return ConflictResult(
            conflicting_dates=[r.date for r in data],
            formateur_conflict=any(r.formateur_id == formateur_id for r in data),
            salle_conflict=any(r.salle_id == salle_id for r in data),
        )

    async def bulk_insert(self, data: list[SOccurrenceEntity]):
        db_models = [self._to_orm(entity) for entity in data]

        self.db.add_all(db_models)

        await self.db.flush()
