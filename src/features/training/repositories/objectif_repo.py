from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from src.db.repositories.base_repository import BaseRepository
from src.features.training.domain.objectif import Objectif as ObjectifEntity
from src.features.training.models.objectif import Objectif as ObjectifDB


class ObjectifRepository(BaseRepository[ObjectifEntity, ObjectifDB]):
    model = ObjectifDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_course_objectifs(self, course_id: UUID) -> list[ObjectifEntity]:
        stmt = select(ObjectifDB).where(ObjectifDB.formation_id == course_id)

        results = await self.db.execute(stmt)

        data = results.scalars()

        return [ObjectifEntity.to_domain(obj) for obj in data]

    def _to_domain(self, orm: ObjectifDB) -> ObjectifEntity:
        return ObjectifEntity(
            id=orm.id, formation_id=orm.formation_id, titre=orm.titre, order=orm.order
        )

    def _to_orm(self, entity: ObjectifEntity) -> ObjectifDB:
        return ObjectifDB(
            id=entity.id,
            titre=entity.titre,
            formation_id=entity.formation_id,
            order=entity.order,
        )
