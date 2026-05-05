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

    if op.session_plan_id:
        from src.features.crm.repository.session_plan_repo import SessionPlanRepo

        sp_repo = SessionPlanRepo(uc.repo.db)

        sp = await sp_repo.get_by_id(op.session_plan_id)

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


from src.features.crm.repository.session_plan_repo import SessionPlanRepo
from src.features.crm.usecases.session_plan_uc import SessionPlanUC
from src.features.crm.schemas.session_plan import (
    CreateSessionPlan,
    ReadSessionPlan,
    UpdateSessionPlan,
)


def get_session_repo(db: AsyncSession = Depends(get_db)):
    return SessionPlanRepo(db)


def get_session_uc(repo: SessionPlanRepo = Depends(get_session_repo)):
    return SessionPlanUC(repo)


@router.post("/{opportunity_id}/session_plan/")
async def create_session_plan(
    opportunity_id: str,
    data: CreateSessionPlan,
    uc: SessionPlanUC = Depends(get_session_uc),
):
    session_plan = await uc.create_session_plan(opportunity_id, data)

    return ReadSessionPlan.model_validate(session_plan)


@router.get("/{opportunity_id}/session_plan")
async def get_opportunity_session_plan(
    opportunity_id: str,
    uc: SessionPlanUC = Depends(get_session_uc),
):
    session_plan = await uc.get_session_plan(opportunity_id)

    return ReadSessionPlan.model_validate(session_plan)


@router.patch("/session_plans/{session_plan}/")
async def update_session_plan(
    session_plan: str,
    data: UpdateSessionPlan,
    uc: SessionPlanUC = Depends(get_session_uc),
):
    updated = await uc.update(UUID(session_plan), data)
    return ReadSessionPlan.model_validate(updated)


@router.patch("/session_plans/{session_plan}/submit/")
async def submit_session_plan(
    session_plan: str,
    uc: SessionPlanUC = Depends(get_session_uc),
):
    updated = await uc.submit_session_plan(UUID(session_plan))
    return ReadSessionPlan.model_validate(updated)
