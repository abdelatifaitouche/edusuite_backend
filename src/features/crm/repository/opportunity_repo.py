from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.features.crm.models.opportunity import Opportunity as OpportunityDB
from src.features.crm.domaine.opportunity import Opportunity as OpportunityEntity
from src.features.crm.filters.opportunity_filters import OpportunityFilters


class OpportunityRepo(BaseRepository[OpportunityEntity, OpportunityDB]):
    model = OpportunityDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _apply_filters(self, stmt, filters: OpportunityFilters):
        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)
        return stmt

    def _to_domain(self, orm: OpportunityDB) -> OpportunityEntity:
        return OpportunityEntity(
            id=orm.id,
            title=orm.title,
            status=orm.status,
            estimated_value=orm.estimated_value,
            probability=orm.probability,
            expected_close_date=orm.expected_close_date,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def _to_orm(self, entity: OpportunityEntity) -> OpportunityDB:
        return OpportunityDB(
            id=entity.id,
            title=entity.title,
            status=entity.status,
            probability=entity.probability,
            estimated_value=entity.estimated_value,
            expected_close_date=entity.expected_close_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def _orm_update(
        self, orm: OpportunityDB, entity: OpportunityEntity
    ) -> OpportunityDB:

        if entity.status:
            orm.status = entity.status
        return orm
