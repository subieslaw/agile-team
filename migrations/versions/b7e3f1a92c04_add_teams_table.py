"""add_teams_table

Revision ID: a1b2c3d4e5f6
Revises: e0e29e712e09
Create Date: 2026-04-25 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b7e3f1a92c04"
down_revision: str | None = "e0e29e712e09"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ts = sa.DateTime(timezone=True)
_now = sa.text("(CURRENT_TIMESTAMP)")


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("created_at", _ts, server_default=_now, nullable=False),
        sa.Column("updated_at", _ts, server_default=_now, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.drop_column("team_members", "team")
    op.add_column(
        "team_members",
        sa.Column("team_id", sa.String(length=36), nullable=True),
    )
    op.create_foreign_key(
        "fk_team_members_team_id",
        "team_members",
        "teams",
        ["team_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_team_members_team_id", "team_members", type_="foreignkey")
    op.drop_column("team_members", "team_id")
    op.add_column(
        "team_members",
        sa.Column("team", sa.String(length=100), nullable=True),
    )
    op.drop_table("teams")
