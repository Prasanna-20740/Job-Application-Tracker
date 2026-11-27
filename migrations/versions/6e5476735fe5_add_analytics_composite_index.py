
"""Add analytics composite index

Revision ID: 6e5476735fe5
Revises: 4ab551010053
"""

from alembic import op


revision = '6e5476735fe5'
down_revision = '4ab551010053'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        'ix_job_application_user_status_applied_date',
        'job_application',
        ['user_id', 'status', 'applied_date'],
        unique=False
    )


def downgrade():
    op.drop_index(
        'ix_job_application_user_status_applied_date',
        table_name='job_application'
    )
