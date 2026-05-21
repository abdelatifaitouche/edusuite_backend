from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from src.db.repositories.base_repository import BaseRepository
from src.features.training.domain.session import (
    Session as SessionEntity,
    SessionDetails,
)
from src.features.training.domain.session_occurrence import (
    SessionOccurence as SOccurrence,
)
from src.features.training.models.session import Session as SessionDB
from src.features.training.models.session_occurrence import SessionOccurrence
from sqlalchemy.orm import joinedload, selectinload


class SessionRepository(BaseRepository[SessionEntity, SessionDB]):
    model = SessionDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _to_domain(self, orm: SessionDB) -> SessionEntity:
        return SessionEntity(
            id=orm.id,
            session_number=orm.reference,
            formation_id=orm.formation_id,
            formateur_id=orm.formateur_id,
            start_date=orm.date_debut,
            end_date=orm.date_fin,
            salle_id=orm.salle_id,
            type_planinng=orm.planning_type,
            status=orm.status,
        )

    def _to_orm(self, entity: SessionEntity) -> SessionDB:
        return SessionDB(
            formation_id=entity.formation_id,
            formateur_id=entity.formateur_id,
            date_debut=entity.start_date,
            date_fin=entity.end_date,
            salle_id=entity.salle_id,
            planning_type=entity.type_planinng,
        )

    async def get_session_details(self, session_id: UUID):

        stmt = (
            select(SessionDB)
            .where(SessionDB.id == session_id)
            .options(
                joinedload(SessionDB.formateur),
                joinedload(SessionDB.formation),
                selectinload(SessionDB.session_occurence),
            )
        )

        result = await self.db.execute(stmt)

        data = result.scalar_one_or_none()

        if data is None:
            raise

        return SessionDetails(
            formateur_name=data.formateur.nom,
            formateur_id=data.formateur_id,
            formation_title=data.formation.titre,
            formation_id=data.formation_id,
            start_date=data.date_debut,
            end_date=data.date_fin,
            status=data.status,
            type_planning=data.planning_type,
            session_number=data.reference,
            id=data.id,
            occurrences=[SOccurrence.to_domain(d) for d in data.session_occurence],
        )

    async def _orm_update(self, orm: SessionDB, entity: SessionEntity):

        if entity.status:
            orm.status = entity.status

        return orm
