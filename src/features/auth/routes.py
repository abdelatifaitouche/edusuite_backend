from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.auth.schemas.user import (
    UserResponse,
    LoginUser,
    CreateUser,
    UserUpdate,
)
from src.db.session import get_db
from src.features.auth.usecases.auth_service import AuthUC
from src.api.dependencies.context import get_context, get_auth_context
from src.core.request_context import RequestContext
from src.features.auth.repository.auth_repository import AuthRepository

from uuid import UUID

router = APIRouter(prefix="/auth")


def get_repo(db: AsyncSession = Depends(get_db)):
    return AuthRepository(db)


def get_service(repo: AuthRepository = Depends(get_repo)):
    return AuthUC(repo)


@router.post("/create_user/")
async def create_user(
    data: CreateUser,
    ctx: RequestContext = Depends(get_auth_context),
    uc: AuthUC = Depends(get_service),
):
    user = await uc.create_user(data)
    return UserResponse.model_validate(user)


@router.post("/login/")
async def login_user(
    data: LoginUser,
    response: Response,
    ctx: RequestContext = Depends(get_context),
    uc: AuthUC = Depends(get_service),
):

    token: str = await uc.login_user(data)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # change to true for https
        samesite="lax",
    )

    return {"message": "Logged In"}


@router.get("/user/{user_id}")
async def get_user_by_id(user_id: str, uc: AuthUC = Depends(get_service)):
    user = await uc.get_by_id(UUID(user_id))

    return UserResponse.model_validate(user)


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
async def list_users(
    ctx: RequestContext = Depends(get_context), uc: AuthUC = Depends(get_service)
):
    users = await uc.list(ctx.pagination)
    return [UserResponse.model_validate(user) for user in users]


@router.delete("/user/{user_id}")
async def delete_user(user_id: str, uc: AuthUC = Depends(get_service)):
    return await uc.delete(UUID(user_id))


@router.patch("/user/{user_id}/")
async def update_user(
    user_id: str,
    data: UserUpdate,
    uc: AuthUC = Depends(get_service),
):
    user = await uc.update(UUID(user_id), data)
    return UserResponse.model_validate(user)


def block_user():
    return
