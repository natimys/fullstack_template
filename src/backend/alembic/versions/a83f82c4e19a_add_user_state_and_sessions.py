"""Add account state and session revocation version."""

from alembic import op
import sqlalchemy as sa

revision = "a83f82c4e19a"
down_revision = "fdee927134bd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("session_version", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("users", "session_version")
