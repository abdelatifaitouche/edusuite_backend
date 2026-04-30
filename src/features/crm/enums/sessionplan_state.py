from enum import StrEnum


class SessionPlanStatus(StrEnum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    LOCKED = "LOCKED"


class LocationType(StrEnum):
    IN_HOUSE = "IN_HOUSE"
    HOTEL = "HOTEL"
