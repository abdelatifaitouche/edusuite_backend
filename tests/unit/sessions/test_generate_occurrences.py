import pytest
import uuid
from datetime import date, time
from src.features.training.domain.reccurence_rule import SessionRecurence
from src.features.training.domain.session import Session
from src.features.training.domain.session_occurrence import SessionOccurence
from src.features.training.enums.session import (
    SessionState,
    SessionOccurenceState,
    PlanningType,
)

from src.features.training.orchestrators.session_orchestrator import SessionOrchestrator


s_orch = SessionOrchestrator(None, None)


@pytest.fixture
def session():
    return Session(
        id=uuid.uuid4(),
        formation_id=uuid.uuid4(),
        formateur_id=uuid.uuid4(),
        salle_id=uuid.uuid4(),
        start_date=date(2026, 5, 18),
        end_date=date(2026, 6, 2),
        type_planinng=PlanningType.BLOC,
    )


@pytest.fixture
def r_rule(session: Session):
    if not session.id:
        raise
    return SessionRecurence(
        id=uuid.uuid4(),
        session_id=session.id,
        jours=[0, 1],
        start_at=time(8, 0),
        end_at=time(10, 0),
        weeks_interval=2,
    )


def test_session_weeks(session, r_rule):
    oc = s_orch.get_weeks(session.start_date, session.end_date, r_rule.weeks_interval)

    assert oc == 2


def test_session_occurences_number(session, r_rule):
    n_oc = s_orch.generate_occurrences(session, r_rule)
    assert len(n_oc) == 4


def test_session_occurrences_dates(session, r_rule):
    oc = s_orch.generate_occurrences(session, r_rule)

    assert oc[0].planned_date == session.start_date
    assert oc[1].planned_date == date(2026, 5, 19)

    assert oc[2].planned_date == date(2026, 6, 1)
    assert oc[3].planned_date == date(2026, 6, 2)
