from sqlalchemy.ext.asyncio import AsyncSession
from src.core.pagination import Pagination
from src.features.auth.schemas.jwt_payload import JwtPayload


class RequestContext:
    def __init__(
        self, db: AsyncSession, pagination: Pagination, user: JwtPayload | None = None
    ):
        self.user: JwtPayload | None = user
        self.db: AsyncSession = db
        self.pagination: Pagination = pagination

    def is_authenticated(self):
        return

    def has_permission(self):
        return

    def require_permissions(self):
        return
