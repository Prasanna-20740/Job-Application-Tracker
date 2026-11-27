
"""Fix application status enum type name

Revision ID: 4ab551010053
Revises: a0e241522939
"""

from alembic import op

revision = '4ab551010053'
down_revision = 'a0e241522939'
branch_labels = None
depends_on = None


def upgrade():
    # Rename old PostgreSQL ENUM type to match app.py
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'applicationstatus'
            )
            AND NOT EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'application_status'
            )
            THEN
                ALTER TYPE applicationstatus
                RENAME TO application_status;
            END IF;
        END
        $$;
    """)


def downgrade():
    # Restore the original ENUM type name
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'application_status'
            )
            AND NOT EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'applicationstatus'
            )
            THEN
                ALTER TYPE application_status
                RENAME TO applicationstatus;
            END IF;
        END
        $$;
    """)
