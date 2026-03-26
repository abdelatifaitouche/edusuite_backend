from src.core.request_context import RequestContext
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db


def get_context(db: AsyncSession = Depends(get_db)) -> RequestContext:
    return RequestContext(db)
