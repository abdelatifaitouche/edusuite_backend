from sqlalchemy.ext.asyncio import AsyncSession
from src.db.usecases.base_usecase import BaseUC
from src.core.pagination import Pagination
from src.features.auth.schemas.user import (
    CreateUser,
    LoginUser,
    UserResponse,
    UserUpdate,
)
from src.features.auth.security.password import PasswordManager
from src.features.auth.repository.auth_repository import AuthRepository
from src.features.auth.models.users import UserModel
from src.features.auth.exceptions import WrongCredentialsError, UserAlreadyExistsError
from src.core.request_context import RequestContext
from src.features.auth.security.jwt import JwtManager
from src.features.auth.schemas.jwt_payload import JwtPayload


from src.features.auth.domain.user import User as UserEntity


class AuthUC(BaseUC[UserEntity, CreateUser, UserUpdate]):
    def __init__(self, repo: AuthRepository):
        super().__init__(repo=repo)
        self.repo: AuthRepository = repo
        self.pwd_manager: PasswordManager = PasswordManager()
        self.jwt_manager: JwtManager = JwtManager()

    def _to_entity(self, data: CreateUser) -> UserEntity:
        user: UserEntity = UserEntity(
            email=data.email,
            role=data.role,
            hashed_password=data.password,
        )
        return user

    async def _apply_update(self, entity: UserEntity, data: UserUpdate) -> UserEntity:
        if data.email:
            entity.email = data.email

        if data.role:
            entity.role = data.role

        if data.is_active:
            entity.is_active = data.is_active

        return entity

    async def create_user(self, data: CreateUser) -> UserEntity:
        user: UserEntity | None = await self.repo.get_by_email(data.email)

        if user:
            raise UserAlreadyExistsError(data.email)

        hashed_password: str = self.pwd_manager.hash_password(data.password)

        user_model: UserModel = UserModel(
            email=data.email, password=hashed_password, role=data.role
        )

        user_entity: UserEntity = self._to_entity(data)

        user_entity = await self.repo.save(user_entity)

        return user_entity

    async def login_user(self, data: LoginUser) -> str:

        user: UserEntity | None = await self.repo.get_by_email(data.email)

        if not user:
            raise WrongCredentialsError()

        if not user.hashed_password or not self.pwd_manager.verify_password(
            data.password, user.hashed_password
        ):
            raise WrongCredentialsError()

        access_token: str = self.jwt_manager.generate_token(
            JwtPayload(id=user.id, email=user.email, role=user.role),
        )

        return access_token
