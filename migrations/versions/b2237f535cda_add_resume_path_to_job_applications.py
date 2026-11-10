"""Add resume path to job applications

Revision ID: b2237f535cda
Revises: 894bd24d4fd9
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = 'b2237f535cda'
down_revision = '894bd24d4fd9'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        'job_application',
        sa.Column(
            'resume_path',
            sa.String(length=255),
            nullable=True
        )
    )


def downgrade():

    op.drop_column(
        'job_application',
        'resume_path'
    )