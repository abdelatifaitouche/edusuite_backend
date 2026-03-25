from src.features.crm.models.companies import CompanyModel
from src.features.crm.schemas.company import CompanyCreate, CompanyRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import Select


class CompanyRepository:
    async def list(self, db: AsyncSession) -> list[CompanyRead]:
        stmt = select(CompanyModel)

        results = await db.execute(stmt)

        companies = results.scalars().all()

        return [CompanyRead.from_orm(company) for company in companies]

    def get_by_id(self):
        return

    async def save(self, db: AsyncSession, data: CompanyCreate) -> CompanyRead:
        company: CompanyModel = CompanyModel(**data.dict())

        db.add(company)

        await db.flush()

        return CompanyRead.from_orm(company)

    def delete(self):
        return
