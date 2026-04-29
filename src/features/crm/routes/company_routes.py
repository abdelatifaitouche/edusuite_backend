from fastapi import APIRouter, Depends
from src.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.crm.usecases.company_usecase import CompanyUC
from src.features.crm.schemas.company import CompanyRead, CompanyCreate
from src.core.pagination import Pagination
from src.api.dependencies.context import get_context
from src.core.request_context import RequestContext


router = APIRouter(prefix="/companies", tags=["crm"])


@router.get("/companies", response_model=list[CompanyRead])
async def list_companies(ctx: RequestContext = Depends(get_context)):
    uc = CompanyUC()
    return await uc.list(ctx)


@router.post("/companies/create/", response_model=CompanyRead)
async def create_company(
    data: CompanyCreate, ctx: RequestContext = Depends(get_context)
):
    uc = CompanyUC()
    return await uc.create(ctx, data)


@router.get("/companies/{company_id}")
async def get_company_by_id(
    company_id: str, ctx: RequestContext = Depends(get_context)
):
    uc = CompanyUC()
    return await uc.get_by_id(ctx, company_id)


@router.delete("/companies/{company_id}")
async def delete_company(company_id: str, ctx: RequestContext = Depends(get_context)):
    uc = CompanyUC()
    return await uc.delete(company_id)
