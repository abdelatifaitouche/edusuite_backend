from datetime import timedelta, date
import math
from src.features.training.usecases.sessionUC import SessionUC
from src.features.training.usecases.reccurrence_ruleUC import RRuleUC
from src.features.training.schemas.session import CreateSession
from src.features.training.schemas.session_reccurrence import CreateRecurrenceRule
from src.features.training.domain.session import Session as SessionEntity
from src.features.training.domain.session_occurrence import SessionOccurence
from src.features.training.domain.reccurence_rule import SessionRecurence
from src.features.training.enums.session import SessionOccurenceState
from src.features.training.repositories.occurrence_repo import OccurrenceRepository


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

    def get_weeks(self, start_date, end_date, interval) -> int:
        return math.ceil((end_date - start_date).days / (7 * interval))

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
        # availibility checl

        session: SessionEntity = await self.session_service.create(data)
        if session.id is None:
            raise

        data.r_rule.session_id = session.id
        rrule: SessionRecurence = await self.rule_service.create(data.r_rule)

        s_occurences: list[SessionOccurence] = self.generate_occurrences(session, rrule)

        await self.s_occ_repo.bulk_insert(s_occurences)

        return session
