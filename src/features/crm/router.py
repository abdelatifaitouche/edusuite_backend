from fastapi import APIRouter, Depends
from src.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.usecases.company_usecase import CompanyUseCases
from src.features.crm.schemas.company import CompanyRead, CompanyCreate


def get_service(db: AsyncSession = Depends(get_db)):
    return CompanyUseCases(db)


router = APIRouter(prefix="/crm", tags=["crm"])


@router.get("/companies", response_model=list[CompanyRead])
async def list_companies(service: CompanyUseCases = Depends(get_service)):
    return await service.list()


@router.post("/companies/create/", response_model=CompanyRead)
async def create_company(
    data: CompanyCreate, service: CompanyUseCases = Depends(get_service)
):
    return await service.create(data)


@router.get("/companies/{company_id}")
async def get_company_by_id(
    company_id: str, service: CompanyUseCases = Depends(get_service)
):
    return await service.get_by_id(company_id)


@router.delete("/companies/{company_id}")
async def delete_company(
    company_id: str, service: CompanyUseCases = Depends(get_service)
):
    return await service.delete(company_id)
