from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlalchemy import insert, text, bindparam, update, select
from src.db.repositories.base_repository import BaseRepository
from src.features.training.domain.session_occurrence import (
    SessionOccurence as SOccurrenceEntity,
    ConflictResult,
    SessionOccurrenceCompact as SOCompactEntity,
)
from src.features.training.models.session_occurrence import (
    SessionOccurrence as SOccurrenceDB,
)
from src.features.training.filters.session_occurrences import OccurrenceFilters
from src.core.pagination import Pagination


class OccurrenceRepository(BaseRepository[SOccurrenceEntity, SOccurrenceDB]):
    model = SOccurrenceDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _apply_filters(self, stmt, filters: OccurrenceFilters):

        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)

        if filters.start_date and filters.end_date:
            stmt = stmt.where(
                self.model.date >= filters.start_date,
                self.model.date <= filters.end_date,
            )

        return stmt

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

    async def list_calendar(self, pagination: Pagination, filters: OccurrenceFilters):
        from src.features.training.models.session import Session as SessionDB
        from src.features.training.models.formateur import Formateur as FormateurDB
        from src.features.training.models.formation import Formation as FormationDB

        stmt = (
            select(
                self.model.id,
                self.model.date,
                self.model.status,
                self.model.start_at,
                self.model.end_at,
                SessionDB.id.label("session_id"),
                SessionDB.session_number,
                FormationDB.titre.label("formation_titre"),
                FormateurDB.nom.label("formateur_nom"),
            )
            .join(SessionDB, SessionDB.id == self.model.session_id)
            .join(FormationDB, FormationDB.id == SessionDB.formation_id)
            .join(FormateurDB, FormateurDB.id == SessionDB.formateur_id)
        )
        stmt = self._apply_filters(stmt, filters)
        result = await self.db.execute(stmt)

        data = result.all()

        return [
            SOCompactEntity(
                session_number=d.session_number,
                formateur_name=d.formateur_nom,
                formation_name=d.formation_titre,
                planned_date=d.date,
                id=d.id,
                start_at=d.start_at,
                end_date=d.end_at,
                status=d.status,
                session_id=d.session_id,
            )
            for d in data
        ]

    async def get_session_occurences(self, session_id: UUID):

        stmt = select(self.model).where(self.model.session_id == session_id)

        result = await self.db.execute(stmt)

        data = result.scalars()

        return [self._to_domain(d) for d in data]

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

    async def cancel_occurrences(self, session_id: UUID):
        from src.features.training.enums.session import SessionOccurenceState

        stmt = (
            update(self.model)
            .where(self.model.session_id == session_id)
            .values(status=SessionOccurenceState.CANCELLED)
        )
        result = await self.db.execute(stmt)

    async def bulk_insert(self, data: list[SOccurrenceEntity]):
        db_models = [self._to_orm(entity) for entity in data]

        self.db.add_all(db_models)

        await self.db.flush()
