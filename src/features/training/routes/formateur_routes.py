from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from src.db.session import get_db
from src.core.pagination import Pagination

from src.features.training.usecases.formateurUC import FormateurUC
from src.features.training.repositories.formateur_repo import FormateurRepo
from src.features.training.schemas.formateur import (
    FormateurCreate,
    FormateurRead,
    FormateurUpdate,
    FormateurSummary,
)
from src.features.training.filters.formateur_filters import FormateurFilters
from src.features.training.schemas.formation import ReadFormation

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
    trainers = await uc.list_trainers(pagination, filters)
    return [FormateurSummary.model_validate(trainer) for trainer in trainers]


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
    from src.features.training.schemas.formateur import ReadMiniCourse

    trainer = await uc.get_details(UUID(trainer_id))

    return FormateurRead.model_validate(trainer)


@router.patch("/trainer/{trainer_id}/")
async def update_trainer(
    trainer_id: str,
    data: FormateurUpdate,
    uc: FormateurUC = Depends(get_service),
):
    trainer = await uc.update(UUID(trainer_id), data)
    return FormateurRead.model_validate(trainer)


@router.post("/trainer/{trainer_id}/courses/{course_id}/")
async def add_formation_to_formateur(
    trainer_id: str,
    course_id: str,
    uc: FormateurUC = Depends(get_service),
):
    response = await uc.add_course_to_trainer(UUID(trainer_id), UUID(course_id))
    return response


@router.get("/trainer/{trainer_id}/courses")
async def get_trainer_courses(
    trainer_id: str,
    uc: FormateurUC = Depends(get_service),
):
    courses = await uc.get_trainer_courses(UUID(trainer_id))
    return [ReadFormation.model_validate(course) for course in courses]


@router.post("/trainer/{trainer_id}/block/")
async def block_trainer(
    trainer_id: str,
    uc: FormateurUC = Depends(get_service),
):
    trainer = await uc.block_trainer(UUID(trainer_id))
    return FormateurRead.model_validate(trainer)
