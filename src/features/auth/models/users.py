from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, Boolean
from src.db.base import Base
from src.core.enums.role import Role


class UserModel(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(Enum(Role, name="user_role_enum"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
