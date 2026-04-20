from pydantic import BaseModel, Field
from src.core.enums.role import Role
from uuid import UUID


class LoginUser(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    role: Role

    model_config = {"from_attributes": True}


class CreateUser(BaseModel):
    email: str
    password: str = Field(min_length=8)

    role: Role
