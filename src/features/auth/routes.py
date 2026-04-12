from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.auth.schemas.user import BaseUser, LoginUser, CreateUser
from src.db.session import get_db
from src.features.auth.usecases.auth_service import AuthService
from src.api.dependencies.context import get_context
from src.core.request_context import RequestContext

router = APIRouter(prefix="/auth")


@router.post("/create_user/")
async def create_user(data: CreateUser, ctx: RequestContext = Depends(get_context)):
    uc = AuthService(ctx.db)
    user: BaseUser = await uc.create_user(data)
    return user


def login_user():
    return


def me():
    return


def get_user_by_id():
    return


@router.get("/list_users")
async def list_users(ctx: RequestContext = Depends(get_context)):
    uc = AuthService(ctx.db)
    users = await uc.list_users(ctx)
    return users


def delete_user():
    return


def update_user():
    return


def block_user():
    return
