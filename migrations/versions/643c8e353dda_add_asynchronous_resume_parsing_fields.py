
"""add asynchronous resume parsing fields

Revision ID: 643c8e353dda
Revises: 8ff8e1a93506
Create Date: 2026-11-24 11:48:31.137427

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "643c8e353dda"
down_revision = "8ff8e1a93506"
branch_labels = None
depends_on = None


def upgrade():

    # Add asynchronous resume parsing fields.
    # Existing columns and records remain unchanged.

    op.add_column(
        "job_application",
        sa.Column(
            "resume_text",
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        "job_application",
        sa.Column(
            "resume_skills",
            sa.JSON(),
            nullable=True
        )
    )

    op.add_column(
        "job_application",
        sa.Column(
            "resume_parse_status",
            sa.String(length=20),
            nullable=False,
            server_default="NOT_STARTED"
        )
    )

    op.add_column(
        "job_application",
        sa.Column(
            "resume_parsed_at",
            sa.DateTime(),
            nullable=True
        )
    )


def downgrade():

    # Remove only the four Day 16 columns.

    op.drop_column(
        "job_application",
        "resume_parsed_at"
    )

    op.drop_column(
        "job_application",
        "resume_parse_status"
    )

    op.drop_column(
        "job_application",
        "resume_skills"
    )

    op.drop_column(
        "job_application",
        "resume_text"
    )
