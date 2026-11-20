
"""add user role enum

Revision ID: be861282aab0
Revises: 70a60851e7bc
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "be861282aab0"
down_revision = "70a60851e7bc"
branch_labels = None
depends_on = None


def upgrade():
    # Create PostgreSQL USER / ADMIN enum
    user_role_enum = postgresql.ENUM(
        "USER",
        "ADMIN",
        name="user_role",
        create_type=False
    )

    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Add role column with USER as default for existing users
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
            server_default=sa.text("'USER'::user_role")
        )
    )

    # Remove server-side default after existing rows are populated
    op.alter_column(
        "users",
        "role",
        existing_type=user_role_enum,
        server_default=None
    )


def downgrade():
    user_role_enum = postgresql.ENUM(
        "USER",
        "ADMIN",
        name="user_role",
        create_type=False
    )

    op.drop_column("users", "role")
    user_role_enum.drop(op.get_bind(), checkfirst=True)
