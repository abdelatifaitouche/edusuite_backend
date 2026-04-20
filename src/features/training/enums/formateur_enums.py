from enum import StrEnum


class NiveauExpertise(StrEnum):
    junior = "junior"
    confirme = "confirme"
    senior = "senior"
    expert = "expert"


class FormateurStatus(StrEnum):
    ACTIVE = "ACTIVE"
    NON_ACTIVE = "NON_ACTIVE"


class RoleFormateur(StrEnum):
    principal = "principal"
    co_formateur = "co_formateur"
    remplacant = "remplacant"
    superviseur = "superviseur"
