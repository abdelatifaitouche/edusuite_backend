from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.auth.schemas.user import BaseUser, LoginUser, CreateUser
from src.db.session import get_db
from src.features.auth.usecases.auth_service import AuthService
from src.api.dependencies.context import get_context, get_auth_context
from src.core.request_context import RequestContext

router = APIRouter(prefix="/auth")


@router.post("/create_user/")
async def create_user(
    data: CreateUser,
    ctx: RequestContext = Depends(get_auth_context),
):
    uc = AuthService(ctx.db)
    user: BaseUser = await uc.create_user(data)
    return user


@router.post("/login/")
async def login_user(
    data: LoginUser, response: Response, ctx: RequestContext = Depends(get_context)
):
    uc = AuthService(ctx.db)

    token: str = await uc.login_user(data)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # change to true for https
        samesite="lax",
    )

    return {"message": "Logged In"}


@router.get("/me")
async def me(ctx: RequestContext = Depends(get_auth_context)):
    return ctx.user


@router.post("/logout/")
async def logout(response: Response, ctx: RequestContext = Depends(get_auth_context)):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )
    return {"message": "Logged out"}


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
