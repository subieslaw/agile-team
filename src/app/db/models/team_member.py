from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, new_uuid


class TeamMember(Base, TimestampMixin):
    __tablename__ = "team_members"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    team_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("teams.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    team_rel: Mapped["Team | None"] = relationship(  # noqa: F821
        "Team", back_populates="members", foreign_keys=[team_id]
    )
    member_skills: Mapped[list["MemberSkill"]] = relationship(  # noqa: F821
        "MemberSkill", back_populates="member", cascade="all, delete-orphan"
    )
