from dataclasses import dataclass
from uuid import UUID
from datetime import time


@dataclass
class SessionRecurence:
    session_id: UUID
    jours: list[int]
    start_at: time
    end_at: time
    weeks_interval: int = 1  # each week
    id: UUID | None = None
