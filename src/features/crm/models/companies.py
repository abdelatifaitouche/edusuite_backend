from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from .company_enums import OrgType, ActivitySector, CompanyStatus
from sqlalchemy import Enum, String, Text, Index


class CompanyModel(Base):
    __tablename__ = "companies"

    # Legal & Commercial Names
    legal_name: Mapped[str] = mapped_column(
        "raison_sociale",
        String(150),
        nullable=False,
        index=True,
    )

    trade_name: Mapped[str] = mapped_column(
        "nom_commercial",
        String(150),
        nullable=True,
        index=True,
    )

    organization_type: Mapped[OrgType] = mapped_column(
        Enum(OrgType, name="org_type_enum"),
        nullable=False,
        index=True,
    )

    activity_sector: Mapped[ActivitySector] = mapped_column(
        Enum(ActivitySector, name="activity_sector_enum"),
        nullable=False,
    )

    status: Mapped[CompanyStatus] = mapped_column(
        Enum(CompanyStatus, name="company_status_enum"),
        nullable=False,
        default=CompanyStatus.ACTIVE,
        index=True,
    )

    # ───────────── Contact Info ─────────────
    website: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(150))

    # ───────────── Legal Identifiers ─────────────
    rc_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nif_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    ai_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("ix_companies_legal_name", "raison_sociale"),
        Index("ix_companies_trade_name", "nom_commercial"),
    )
