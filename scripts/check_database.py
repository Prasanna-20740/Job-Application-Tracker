
import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import app as m
from sqlalchemy import text

with m.app.app_context():

    m.db.session.rollback()

    print("\n--- BENCHMARK USERS ---")

    users = m.User.query.filter(
        m.User.username.like("benchmark_%")
    ).all()

    for user in users:
        print(user.id, user.username, user.email)

    print("\n--- POSTGRES ENUM TYPES ---")

    query = text("""
        SELECT t.typname
        FROM pg_type t
        JOIN pg_namespace n ON n.oid = t.typnamespace
        WHERE t.typtype = 'e'
        AND n.nspname = 'public'
        ORDER BY t.typname
    """)

    results = m.db.session.execute(query)

    for row in results:
        print(row[0])

    print("\n--- JOB APPLICATION STATUS COLUMN ---")

    column_query = text("""
        SELECT column_name, data_type, udt_name
        FROM information_schema.columns
        WHERE table_name = 'job_application'
        AND column_name = 'status'
    """)

    column_result = m.db.session.execute(column_query)

    for row in column_result:
        print(
            "Column:", row[0],
            "| Data type:", row[1],
            "| ENUM type:", row[2]
        )

    print("\n--- ALEMBIC REVISION ---")

    revision_query = text(
        "SELECT version_num FROM alembic_version"
    )

    revision_result = m.db.session.execute(revision_query)

    for row in revision_result:
        print(row[0])
