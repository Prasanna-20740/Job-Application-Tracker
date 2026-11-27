
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import app as m
from sqlalchemy import text

BENCHMARK_USERNAME = "benchmark_d474f1fb62a7"
BENCHMARK_EMAIL = "benchmark_d474f1fb62a7@example.com"

with m.app.app_context():
    try:
        user = m.User.query.filter_by(
            username=BENCHMARK_USERNAME,
            email=BENCHMARK_EMAIL
        ).first()

        if user is None:
            print("Benchmark user not found. Nothing to clean.")
        else:
            user_id = user.id

            application_ids = (
                m.db.session.query(m.JobApplication.id)
                .filter_by(user_id=user_id)
            )

            history_count = m.db.session.query(
                m.ApplicationStatusHistory
            ).filter(
                m.ApplicationStatusHistory.application_id.in_(
                    application_ids
                )
            ).delete(synchronize_session=False)

            application_count = m.JobApplication.query.filter_by(
                user_id=user_id
            ).delete(synchronize_session=False)

            m.db.session.delete(user)
            m.db.session.commit()

            print("Benchmark user removed:", user_id)
            print("Applications removed:", application_count)
            print("History records removed:", history_count)

    except Exception:
        m.db.session.rollback()
        raise
