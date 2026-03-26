from pydantic import BaseModel
from src.features.crm.models.company_enums import CompanyStatus, ActivitySector, OrgType
from uuid import UUID


class CompanyCreate(BaseModel):
    legal_name: str
    trade_name: str | None = ""
    organization_type: OrgType = OrgType.ETATIQUE
    activity_sector: ActivitySector = ActivitySector.AUTRES
    website: str | None = ""
    phone: str | None = ""
    email: str | None = ""
    rc_number: str = ""
    nif_number: str = ""
    ai_number: str = ""
    notes: str | None = ""

    model_config = {"from_attributes": True}


class CompanyRead(BaseModel):
    id: UUID
    legal_name: str
    trade_name: str | None = ""
    status: CompanyStatus
    organization_type: OrgType
    activity_sector: ActivitySector
    website: str | None = ""
    phone: str | None = ""
    email: str | None = ""
    rc_number: str = ""
    nif_number: str = ""
    ai_number: str = ""
    notes: str | None = ""

    model_config = {"from_attributes": True}
