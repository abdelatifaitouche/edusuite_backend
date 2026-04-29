from enum import StrEnum


class OpportunityStates(StrEnum):
    NEW = "NEW"
    NEED_ANALYSIS = "NEED_ANALYSIS"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    CANCELLED = "CANCELLED"
