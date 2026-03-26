from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.repository.company_repository import CompanyRepository
from src.features.crm.schemas.company import CompanyRead, CompanyCreate
from uuid import UUID


class CompanyUseCases:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.repo: CompanyRepository = CompanyRepository()

    async def list(self) -> list[CompanyRead]:
        return await self.repo.list(self.db)

    async def create(self, data: CompanyCreate) -> CompanyRead:
        company: CompanyRead = await self.repo.save(self.db, data)
        await self.db.commit()
        return company

    async def get_by_id(self, entity_id: str) -> CompanyRead:
        return await self.repo.get_by_id(self.db, UUID(entity_id))

    async def delete(self, entity_id: str):
        result = await self.repo.delete(self.db, UUID(entity_id))

        if result:
            await self.db.commit()
            return True
        return False

    async def update(self):
        return
