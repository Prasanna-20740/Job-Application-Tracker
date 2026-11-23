
"""add webhook deliveries table

Revision ID: 8ff8e1a93506
Revises: c5fd88f5a837
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8ff8e1a93506"
down_revision = "c5fd88f5a837"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "webhook_deliveries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("target_url", sa.String(length=1000), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("next_retry_at", sa.DateTime(), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_webhook_deliveries_event_type",
        "webhook_deliveries",
        ["event_type"],
        unique=False,
    )

    op.create_index(
        "ix_webhook_deliveries_status",
        "webhook_deliveries",
        ["status"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        "ix_webhook_deliveries_status",
        table_name="webhook_deliveries",
    )

    op.drop_index(
        "ix_webhook_deliveries_event_type",
        table_name="webhook_deliveries",
    )

    op.drop_table("webhook_deliveries")
