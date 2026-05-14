from src.db.usecases.base_usecase import BaseUC
from src.features.training.repositories.reccurrence_repo import ReccurenceRepository
from src.features.training.domain.reccurence_rule import SessionRecurence as RRuleEntity
from src.features.training.schemas.session_reccurrence import (
    CreateRecurrenceRule,
    ReadRecurrenceRule,
)


class RRuleUC(BaseUC[RRuleEntity, CreateRecurrenceRule, ReadRecurrenceRule]):
    def __init__(self, repo: ReccurenceRepository):
        super().__init__(repo)
        self.repo = repo

    def _to_entity(self, data: CreateRecurrenceRule):
        return RRuleEntity(
            session_id=data.session_id,
            jours=data.jours_semaine,
            start_at=data.heure_debut,
            end_at=data.heure_fin,
            weeks_interval=data.intervalle_semaines,
        )
