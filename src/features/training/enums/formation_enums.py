from enum import StrEnum


class TypeFormation(StrEnum):
    POUR_ENTREPRISE = "POUR_ENTREPRISE"
    PARTICULIER = "PARTICULIER"


class NiveauFormation(StrEnum):
    debutant = "debutant"
    intermediaire = "intermediaire"
    avance = "avance"
    tous_niveaux = "tous_niveaux"


class DomainFormation(StrEnum):
    rh = "rh"
    developpement_personnel = "developpement_personnel"
    management = "management"
    team_building = "team_building"
    coaching = "coaching"
    sst = "sst"
    juridique = "juridique"
    informatique = "informatique"
    autre = "autre"


class StatusFormation(StrEnum):
    DISPONIBLE = "DISPONIBLE"
    NON_DISPONIBLE = "NON_DISPONIBLE"
