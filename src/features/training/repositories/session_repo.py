from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.base_repository import BaseRepository
from src.features.training.domain.session import Session as SessionEntity
from src.features.training.models.session import Session as SessionDB


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

    async def _orm_update(self, orm: SessionDB, entity: SessionEntity):

        if entity.status:
            orm.status = entity.status

        return orm
