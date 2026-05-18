from datetime import timedelta, date
from uuid import UUID, uuid4
import math
from src.features.training.usecases.sessionUC import SessionUC
from src.features.training.usecases.reccurrence_ruleUC import RRuleUC
from src.features.training.schemas.session import CreateSession
from src.features.training.schemas.session_reccurrence import CreateRecurrenceRule
from src.features.training.domain.session import Session as SessionEntity
from src.features.training.domain.session_occurrence import (
    SessionOccurence,
    ConflictResult,
)
from src.features.training.domain.reccurence_rule import SessionRecurence
from src.features.training.enums.session import SessionOccurenceState
from src.features.training.repositories.occurrence_repo import OccurrenceRepository
from src.core.exception import SessionConflictError


class SessionOrchestrator:
    def __init__(
        self,
        session_service: SessionUC,
        rule_service: RRuleUC,
        s_occ_repo: OccurrenceRepository,
    ):
        self.session_service: SessionUC = session_service
        self.rule_service: RRuleUC = rule_service
        self.s_occ_repo: OccurrenceRepository = s_occ_repo

    async def assert_no_conflicts(
        self, expected_dates: list[date], formateur_id: UUID, salle_id: UUID
    ) -> None:
        conflicts: ConflictResult | None = await self.s_occ_repo.check_conflicts(
            expected_dates, formateur_id, salle_id
        )

        if not conflicts:
            return

        raise SessionConflictError(
            message="Session conflict detected",
            dates=conflicts.conflicting_dates,
            formateur_conflict=conflicts.formateur_conflict,
            salle_conflict=conflicts.salle_conflict,
        )

    def generate_occurrences(
        self, session: SessionEntity, r_rule: SessionRecurence
    ) -> list[SessionOccurence]:

        if not session.id:
            raise

        s_occurences: list[SessionOccurence] = []
        # we are getting the monday of the first week as an anchor
        anchor = session.start_date - timedelta(days=session.start_date.weekday())

        weeks_offset = 0

        while True:
            start_week = anchor + timedelta(weeks=weeks_offset)

            if start_week > session.end_date:
                break

            for day in sorted(r_rule.jours):
                p_date = start_week + timedelta(days=day)

                if p_date < session.start_date:
                    continue

                if p_date > session.end_date:
                    continue

                s = SessionOccurence(
                    session_id=session.id,
                    start_at=r_rule.start_at,
                    end_at=r_rule.end_at,
                    planned_date=p_date,
                    notes="",
                    status=SessionOccurenceState.PLANNED,
                )

                s_occurences.append(s)
            weeks_offset += r_rule.weeks_interval
        return s_occurences

    async def create_session(self, data: CreateSession):

        draft_session = SessionEntity(
            id=uuid4(),
            formateur_id=data.formateur_id,
            formation_id=data.formation_id,
            salle_id=data.salle_id,
            type_planinng=data.type_planning,
            start_date=data.date_debut,
            end_date=data.date_fin,
        )

        draft_rule = SessionRecurence(
            session_id=draft_session.id,
            jours=data.r_rule.jours_semaine,
            start_at=data.r_rule.heure_debut,
            end_at=data.r_rule.heure_fin,
            weeks_interval=data.r_rule.intervalle_semaines,
        )

        draft_occurences: list[SessionOccurence] = self.generate_occurrences(
            draft_session, draft_rule
        )
        generated_dates = [gen_date.planned_date for gen_date in draft_occurences]

        print(f"Generated Dates : {generated_dates}")

        await self.assert_no_conflicts(
            generated_dates, draft_session.formateur_id, draft_session.salle_id
        )

        session: SessionEntity = await self.session_service.create(data)
        if session.id is None:
            raise

        data.r_rule.session_id = session.id
        rrule: SessionRecurence = await self.rule_service.create(data.r_rule)

        for occ in draft_occurences:
            occ.session_id = session.id

        await self.s_occ_repo.bulk_insert(draft_occurences)

        return session
