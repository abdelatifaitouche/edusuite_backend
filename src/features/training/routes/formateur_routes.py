from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from src.db.session import get_db
from src.core.pagination import Pagination

from src.features.training.usecases.formateurUC import FormateurUC
from src.features.training.repositories.formateur_repo import FormateurRepo
from src.features.training.schemas.formateur import FormateurCreate, FormateurRead
from src.features.training.filters.formateur_filters import FormateurFilters


router = APIRouter(prefix="/trainers")


def get_repo(db: AsyncSession = Depends(get_db)) -> FormateurRepo:
    return FormateurRepo(db)


def get_service(repo: FormateurRepo = Depends(get_repo)) -> FormateurUC:
    return FormateurUC(repo)


@router.get("")
async def list_trainers(
    pagination: Pagination = Depends(),
    filters: FormateurFilters = Depends(),
    uc: FormateurUC = Depends(get_service),
):
    trainers = await uc.list(pagination, filters)
    return [FormateurRead.model_validate(trainer) for trainer in trainers]


@router.post("/trainer/")
async def create_trainer(
    data: FormateurCreate,
    uc: FormateurUC = Depends(get_service),
):
    formateur = await uc.create(data)
    return FormateurRead.model_validate(formateur)


@router.get("/trainer/{trainer_id}")
async def get_trainer(
    trainer_id: str,
    uc: FormateurUC = Depends(get_service),
):
    trainer = await uc.get_by_id(UUID(trainer_id))
    return FormateurRead.model_validate(trainer)


@router.post("/trainer/{trainer_id}/block/")
async def block_trainer(
    trainer_id: str,
    uc: FormateurUC = Depends(get_service),
):
    trainer = await uc.block_trainer(UUID(trainer_id))
    return FormateurRead.model_validate(trainer)
