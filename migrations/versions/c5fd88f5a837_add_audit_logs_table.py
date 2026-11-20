"""add audit logs table

Revision ID: c5fd88f5a837
Revises: be861282aab0
"""

from alembic import op
import sqlalchemy as sa

revision = "c5fd88f5a837"
down_revision = "be861282aab0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_user_id", sa.Integer(), nullable=True),
        sa.Column("actor_username", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("target_user_id", sa.Integer(), nullable=True),
        sa.Column("target_username", sa.String(100), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        )
    )


def downgrade():
    op.drop_table("audit_logs")