from sqlalchemy.ext.asyncio import AsyncSession
from src.core.pagination import Pagination


class RequestContext:
    def __init__(self, db: AsyncSession, pagination: Pagination):
        self.db: AsyncSession = db
        self.pagination: Pagination = pagination

    def is_authenticated(self):
        return

    def has_permission(self):
        return

    def require_permissions(self):
        return
