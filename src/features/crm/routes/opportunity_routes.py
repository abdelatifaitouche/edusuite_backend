from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.db.session import get_db
from src.core.pagination import Pagination
from src.features.crm.repository.opportunity_repo import OpportunityRepo
from src.features.crm.usecases.OpportunityUC import OpportunityUC
from src.features.crm.schemas.opportunity import CreateOpportunity, ReadOpporunity
from src.features.crm.filters.opportunity_filters import OpportunityFilters


router = APIRouter(prefix="/opportunity")


def get_repo(db: AsyncSession = Depends(get_db)):
    return OpportunityRepo(db)


def get_service(
    repo: OpportunityRepo = Depends(get_repo),
):
    return OpportunityUC(repo)


@router.post("")
async def create_opportunity(
    data: CreateOpportunity,
    uc: OpportunityUC = Depends(get_service),
):
    opportunity = await uc.create(data)
    return ReadOpporunity.model_validate(opportunity)


@router.get("")
async def list_opporunities(
    pagination: Pagination = Depends(),
    filters: OpportunityFilters = Depends(),
    uc: OpportunityUC = Depends(get_service),
):
    opportunities = await uc.list(pagination, filters)
    return [ReadOpporunity.model_validate(op) for op in opportunities]


@router.get("/{opportunity_id}")
async def get_opportunity(
    opportunity_id: str,
    uc: OpportunityUC = Depends(get_service),
):
    op = await uc.get_by_id(UUID(opportunity_id))
    return ReadOpporunity.model_validate(op)


@router.post("/{opportunity_id}/transition/next/")
async def transition(
    opportunity_id: str,
    uc: OpportunityUC = Depends(get_service),
):
    entity = await uc.transition(UUID(opportunity_id))
    return ReadOpporunity.model_validate(entity)


@router.delete("/{opportunity_id}/")
async def delete(opportunity_id: str, uc: OpportunityUC = Depends(get_service)):
    op = await uc.delete(UUID(opportunity_id))
    return op


@router.post("/{opportunity_id}/win/")
async def mark_as_won(opportunity_id: str, uc: OpportunityUC = Depends(get_service)):
    op = await uc.mark_as_win(UUID(opportunity_id))
    return ReadOpporunity.model_validate(op)


@router.post("/{opportunity_id}/lost/")
async def mark_as_lost(opportunity_id: str, uc: OpportunityUC = Depends(get_service)):
    op = await uc.mark_as_lost(UUID(opportunity_id))
    return ReadOpporunity.model_validate(op)
