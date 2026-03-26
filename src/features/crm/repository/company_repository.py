from src.features.crm.models.companies import CompanyModel
from src.features.crm.schemas.company import CompanyCreate, CompanyRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.sql import Select
from uuid import UUID


class CompanyRepository:
    async def list(self, db: AsyncSession) -> list[CompanyRead]:
        stmt = select(CompanyModel)

        results = await db.execute(stmt)

        companies = results.scalars().all()

        return [CompanyRead.from_orm(company) for company in companies]

    async def get_by_id(self, db: AsyncSession, entity_id: UUID) -> CompanyRead:
        stmt = select(CompanyModel).where(CompanyModel.id == entity_id)

        result = await db.execute(stmt)

        company = result.scalar_one_or_none()

        return CompanyRead.from_orm(company)

    async def save(self, db: AsyncSession, data: CompanyCreate) -> CompanyRead:
        company: CompanyModel = CompanyModel(**data.dict())

        db.add(company)

        await db.flush()

        return CompanyRead.from_orm(company)

    async def delete(self, db: AsyncSession, entity_id: UUID):
        stmt = delete(CompanyModel).where(CompanyModel.id == entity_id)

        result = await db.execute(stmt)

        return result.rowcount > 0  # type: ignore
