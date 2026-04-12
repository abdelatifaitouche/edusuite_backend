from dataclasses import dataclass
from uuid import UUID


@dataclass
class JwtPayload:
    id: UUID
    email: str
    role: str
