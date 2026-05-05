from enum import StrEnum


class SessionPlanStatus(StrEnum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    SUBMITED = "SUBMITED"
    REJECTED = "REJECTED"
    LOCKED = "LOCKED"


class LocationType(StrEnum):
    IN_HOUSE = "IN_HOUSE"
    HOTEL = "HOTEL"
