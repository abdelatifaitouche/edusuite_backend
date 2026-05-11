from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.features.training.repositories.salle_repo import SalleRepository
from src.features.training.usecases.salleUC import SalleUC
from src.features.training.schemas.salle import SalleCreate, SalleRead, SalleUpdate
from src.core.pagination import Pagination
from src.features.training.filters.salle import SalleFilters

router = APIRouter(prefix="/salles")


def get_repo(
    db: AsyncSession = Depends(get_db),
):
    return SalleRepository(db)


def get_service(
    repo: SalleRepository = Depends(get_repo),
):
    return SalleUC(repo)


@router.get("")
async def list_salles(
    pagination: Pagination = Depends(),
    filters: SalleFilters = Depends(),
    uc: SalleUC = Depends(get_service),
):

    results = await uc.list(pagination, filters)
    return [SalleRead.model_validate(salle) for salle in results]


@router.post("/")
async def create_salle(
    data: SalleCreate,
    uc: SalleUC = Depends(get_service),
):
    result = await uc.create(data)
    return SalleRead.model_validate(result)


@router.get("/{salle_id}")
async def get_salle(
    salle_id: str,
    uc: SalleUC = Depends(get_service),
):
    result = await uc.get_by_id(UUID(salle_id))
    return SalleRead.model_validate(result)


@router.patch("/{salle_id}/")
async def update_salle(
    salle_id: str,
    data: SalleUpdate,
    uc: SalleUC = Depends(get_service),
):
    result = await uc.update(UUID(salle_id), data)
    return result


@router.delete("/{salle_id}/")
async def delete(
    salle_id: str,
    uc: SalleUC = Depends(get_service),
):
    return await uc.delete(UUID(salle_id))
