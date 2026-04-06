from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, SmallInteger, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, new_uuid


class MemberSkill(Base):
    __tablename__ = "member_skills"
    __table_args__ = (UniqueConstraint("member_id", "skill_id", name="uq_member_skill"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    member_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("team_members.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    proficiency: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    years_exp: Mapped[float | None] = mapped_column(Numeric(4, 1), nullable=True)
    noted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    member: Mapped["TeamMember"] = relationship(  # noqa: F821
        "TeamMember", back_populates="member_skills"
    )
    skill: Mapped["Skill"] = relationship(  # noqa: F821
        "Skill", back_populates="member_skills"
    )
