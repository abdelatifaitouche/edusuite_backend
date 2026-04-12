from src.core.request_context import RequestContext
from fastapi import Depends, Cookie, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.core.pagination import Pagination
from src.features.auth.security.jwt import JwtManager
from src.features.auth.schemas.jwt_payload import JwtPayload


_jwt_manager = JwtManager()


async def get_auth_context(
    access_token: str | None = Cookie(None),
    db: AsyncSession = Depends(get_db),
    pagination: Pagination = Depends(),
):

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Credentials or Token",
        )

    try:
        payload: JwtPayload = _jwt_manager.verify_token(access_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentaisl or Token",
        )

    return RequestContext(
        db=db,
        pagination=pagination,
        user=payload,
    )


async def get_context(
    db: AsyncSession = Depends(get_db), pagination: Pagination = Depends()
) -> RequestContext:
    return RequestContext(db, pagination)
