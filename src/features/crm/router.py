from fastapi import APIRouter, Depends
from src.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.usecases.company_usecase import CompanyUseCases
from src.features.crm.schemas.company import CompanyRead, CompanyCreate
from src.core.pagination import Pagination
from src.api.dependencies.context import get_context
from src.core.request_context import RequestContext


def get_service(ctx: RequestContext = Depends(get_context)):
    return CompanyUseCases(ctx)


router = APIRouter(prefix="/crm", tags=["crm"])


@router.get("/companies", response_model=list[CompanyRead])
async def list_companies(
    pagination: Pagination = Depends(),
    service: CompanyUseCases = Depends(get_service),
):
    return await service.list(pagination)


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
