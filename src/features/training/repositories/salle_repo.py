from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.salle import Salle as SalleDB
from src.features.training.domain.salle import Salle as SalleEntity
from src.features.training.filters.salle import SalleFilters


class SalleRepository(BaseRepository[SalleEntity, SalleDB]):
    model = SalleDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _apply_filters(self, stmt, filters: SalleFilters):

        if filters.status:
            stmt = stmt.where(SalleDB.status == filters.status)

        if filters.size:
            stmt = stmt.where(SalleDB.size == filters.size)

        return stmt

    def _to_domain(self, orm: SalleDB) -> SalleEntity:
        return SalleEntity.to_domaine(orm)

    def _to_orm(self, entity: SalleEntity):
        return SalleDB(
            id=entity.id, name=entity.name, size=entity.size, status=entity.status
        )

    async def _orm_update(
        self,
        orm: SalleDB,
        entity: SalleEntity,
    ) -> SalleDB:

        if entity.size:
            orm.size = entity.size

        if entity.name:
            orm.name = entity.name

        if entity.status:
            orm.status = entity.status

        return orm
