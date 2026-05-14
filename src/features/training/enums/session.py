from enum import StrEnum


class PlanningType(StrEnum):
    BLOC = "BLOC"
    RECURRENT = "RECURRENT"


class SessionState(StrEnum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    EN_COURS = "EN_COURS"
    VALIDATION = "VALIDATION"
    VALIDE = "VALIDE"
    TERMINEE = "TERMINEE"
    CANCELLED = "CANCELLED"
    POSTPONED = "POSTPONED"


class SessionOccurenceState(StrEnum):
    PLANNED = "PLANNED"
    ACTIF = "ACTIF"
    TERMINEE = "TERMINEE"
    CANCELLED = "CANCELLED"
