from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.repository.company_repository import CompanyRepository
from src.features.crm.schemas.company import CompanyRead, CompanyCreate
from uuid import UUID
from src.core.pagination import Pagination
from src.core.request_context import RequestContext


class BaseUC:
    async def list(self):
        return

    async def get_by_id(self):
        return

    async def create(self):
        return

    async def update(self):
        return

    async def delete(self):
        return


class CompanyUseCases:
    def __init__(self, ctx: RequestContext):
        self.ctx = ctx
        self.repo: CompanyRepository = CompanyRepository()

    async def list(self, pagination: Pagination) -> list[CompanyRead]:
        return await self.repo.list(self.ctx.db, pagination)

    async def create(self, data: CompanyCreate) -> CompanyRead:
        company: CompanyRead = await self.repo.save(self.ctx.db, data)
        await self.ctx.db.commit()
        return company

    async def get_by_id(self, entity_id: str) -> CompanyRead:
        return await self.repo.get_by_id(self.ctx.db, UUID(entity_id))

    async def delete(self, entity_id: str):
        result = await self.repo.delete(self.ctx.db, UUID(entity_id))

        if result:
            await self.ctx.db.commit()
            return True
        return False

    async def update(self):
        return
