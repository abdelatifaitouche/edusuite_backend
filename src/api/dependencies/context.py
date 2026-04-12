from src.core.request_context import RequestContext
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.core.pagination import Pagination


def get_context(
    db: AsyncSession = Depends(get_db), pagination: Pagination = Depends()
) -> RequestContext:
    return RequestContext(db, pagination)
