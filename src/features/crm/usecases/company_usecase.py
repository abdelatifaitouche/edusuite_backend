from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.repository.company_repository import CompanyRepository
from src.features.crm.schemas.company import CompanyRead, CompanyCreate
from src.features.crm.models.companies import CompanyModel
from uuid import UUID
from src.core.pagination import Pagination
from src.core.request_context import RequestContext


class CompanyUC:
    def __init__(self):
        self.repo: CompanyRepository = CompanyRepository()

    async def list(self, ctx: RequestContext) -> list[CompanyRead]:
        models: list[CompanyModel] = await self.repo.list(ctx)
        return [CompanyRead.model_validate(model) for model in models]

    async def create(self, ctx: RequestContext, data: CompanyCreate) -> CompanyRead:

        company: CompanyModel = CompanyModel(**data.model_dump())

        company: CompanyModel = await self.repo.save(ctx, company)
        return CompanyRead.model_validate(company)

    async def get_by_id(self, ctx: RequestContext, entity_id: str) -> CompanyRead:
        companyModel: CompanyModel = await self.repo.get_by_id(ctx, UUID(entity_id))

        return CompanyRead.model_validate(companyModel)

    async def delete(self, entity_id: str):
        result = await self.repo.delete(self.ctx.db, UUID(entity_id))

        if result:
            await self.ctx.db.commit()
            return True
        return False

    async def update(self):
        return
