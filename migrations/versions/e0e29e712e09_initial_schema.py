"""initial_schema

Revision ID: e0e29e712e09
Revises:
Create Date: 2026-04-02 19:52:24.098090

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e0e29e712e09"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ts = sa.DateTime(timezone=True)
_now = sa.text("(CURRENT_TIMESTAMP)")


def upgrade() -> None:
    op.create_table(
        "skills",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("created_at", _ts, server_default=_now, nullable=False),
        sa.Column("updated_at", _ts, server_default=_now, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "team_members",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=True),
        sa.Column("team", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", _ts, server_default=_now, nullable=False),
        sa.Column("updated_at", _ts, server_default=_now, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "member_skills",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("skill_id", sa.String(length=36), nullable=False),
        sa.Column("proficiency", sa.SmallInteger(), nullable=True),
        sa.Column("years_exp", sa.Numeric(precision=4, scale=1), nullable=True),
        sa.Column("noted_at", _ts, server_default=_now, nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["team_members.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("member_id", "skill_id", name="uq_member_skill"),
    )


def downgrade() -> None:
    op.drop_table("member_skills")
    op.drop_table("team_members")
    op.drop_table("skills")
