"""Add application status history table

Revision ID: 70a60851e7bc
Revises: 75d934de4c0d
"""

from alembic import op
import sqlalchemy as sa

revision = '70a60851e7bc'
down_revision = '75d934de4c0d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'application_status_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column(
            'status',
            sa.Enum(
                'APPLIED',
                'PHONE_SCREEN',
                'INTERVIEW',
                'OFFER',
                'REJECTED',
                name='application_history_status'
            ),
            nullable=False
        ),
        sa.Column('entered_at', sa.DateTime(), nullable=False),
        sa.Column('exited_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['application_id'],
            ['job_application.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        'ix_application_status_history_application_id',
        'application_status_history',
        ['application_id'],
        unique=False
    )


def downgrade():
    op.drop_index(
        'ix_application_status_history_application_id',
        table_name='application_status_history'
    )
    op.drop_table('application_status_history')
