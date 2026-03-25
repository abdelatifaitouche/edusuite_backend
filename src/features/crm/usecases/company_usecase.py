from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.repository.company_repository import CompanyRepository
from src.features.crm.schemas.company import CompanyRead, CompanyCreate


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
