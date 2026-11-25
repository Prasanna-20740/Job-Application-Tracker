
"""Add stale application alert timestamp

Revision ID: a0e241522939
Revises: 643c8e353dda
"""

from alembic import op
import sqlalchemy as sa

revision = 'a0e241522939'
down_revision = '643c8e353dda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'job_application',
        sa.Column('stale_alert_sent_at', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column('job_application', 'stale_alert_sent_at')
