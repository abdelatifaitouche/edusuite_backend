from dataclasses import dataclass
from uuid import UUID
from src.core.enums.role import Role
from datetime import datetime


@dataclass
class User:
    email: str
    role: str
    hashed_password: str | None = None

    id: UUID | None = None
    created_at: datetime | None = None
    is_active: bool | None = None

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
