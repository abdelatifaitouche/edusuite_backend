from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.base_repository import BaseRepository
from src.features.auth.models.users import UserModel
from src.core.request_context import RequestContext
from src.features.auth.domain.user import User as UserEntity


class AuthRepository(BaseRepository[UserEntity, UserModel]):
    model = UserModel

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _to_domain(self, orm: UserModel) -> UserEntity:
        user: UserEntity = UserEntity(
            hashed_password=orm.password,
            id=orm.id,
            email=orm.email,
            role=orm.role,
            created_at=orm.created_at,
        )
        return user

    def _to_orm(self, entity: UserEntity) -> UserModel:
        return UserModel(
            email=entity.email, password=entity.hashed_password, role=entity.role
        )

    async def get_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(stmt)
        user: UserModel | None = result.scalar_one_or_none()
        if not user:
            return None
        return self._to_domain(user)
