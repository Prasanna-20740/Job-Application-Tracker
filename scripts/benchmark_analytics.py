import sys
import time
import statistics
import uuid

from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import date, datetime, timedelta

from app import (
    app,
    db,
    cache,
    User,
    Role,
    JobApplication,
    ApplicationStatus,
    ApplicationStatusHistory,
)

from flask_jwt_extended import create_access_token
from sqlalchemy import event


TOTAL_RECORDS = 10000
# SQL Query Profiling
query_count = 0
query_timings = []
query_statements = []


def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    context._query_start_time = time.perf_counter()


def after_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    global query_count

    elapsed = time.perf_counter() - context._query_start_time

    query_count += 1
    query_timings.append(elapsed * 1000)
    query_statements.append(statement)

statuses = list(ApplicationStatus)

benchmark_user_id = None
application_ids = []


with app.app_context():

    try:
        print("\nCreating benchmark user...")

        unique_id = uuid.uuid4().hex[:12]

        benchmark_user = User(
            username=f"benchmark_{unique_id}",
            email=f"benchmark_{unique_id}@example.com",
            role=Role.USER,
        )

        db.session.add(benchmark_user)
        db.session.commit()

        benchmark_user_id = benchmark_user.id

        print(f"Benchmark user ID: {benchmark_user_id}")

        print(f"\nCreating {TOTAL_RECORDS} applications...")

        applications = []

        for i in range(TOTAL_RECORDS):
            status = statuses[i % len(statuses)]

            applications.append(
                JobApplication(
                    company=f"Benchmark Company {i}",
                    role="Python Developer",
                    status=status,
                    applied_date=date.today() - timedelta(days=i % 30),
                    user_id=benchmark_user_id,
                )
            )

        db.session.add_all(applications)
        db.session.flush()

        application_ids = [item.id for item in applications]

        print("Applications created.")

        print("\nCreating status history records...")

        now = datetime.utcnow()

        history_records = [
            ApplicationStatusHistory(
                application_id=application.id,
                status=application.status,
                entered_at=now - timedelta(days=2),
                exited_at=now,
            )
            for application in applications
        ]

        db.session.add_all(history_records)
        db.session.commit()

        print("History records created.")

        print("\nGenerating JWT token...")

        access_token = create_access_token(
            identity=str(benchmark_user_id)
        )

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
                # Start SQL query profiling
        event.listen(
            db.engine,
            "before_cursor_execute",
            before_cursor_execute
        )

        event.listen(
            db.engine,
            "after_cursor_execute",
            after_cursor_execute
        )

        print("\nSQL query profiling started...")

        print("\nRunning analytics benchmark...")

        cache_key = f"analytics:user:{benchmark_user_id}"

        # Clear existing cache to guarantee a MISS
        cache.delete(cache_key)

        miss_timings = []
        hit_timings = []

        with app.test_client() as client:

            # --------------------------------
            # Measure Cache MISS
            # --------------------------------
            print("\nMeasuring Cache MISS...")

            start = time.perf_counter()

            miss_response = client.get(
                "/api/analytics",
                headers=headers
            )

            end = time.perf_counter()

            if miss_response.status_code != 200:
                raise Exception(
                    f"Cache MISS failed: {miss_response.status_code} "
                    f"{miss_response.get_data(as_text=True)}"
                )

            miss_ms = (end - start) * 1000
            miss_timings.append(miss_ms)

            print(f"Cache MISS: {miss_ms:.2f} ms")

            # --------------------------------
            # Measure Cache HIT (5 requests)
            # --------------------------------
            print("\nMeasuring Cache HIT...")

            for i in range(5):

                start = time.perf_counter()

                response = client.get(
                    "/api/analytics",
                    headers=headers
                )

                end = time.perf_counter()

                if response.status_code != 200:
                    raise Exception(
                        f"Cache HIT request failed: {response.status_code}"
                    )

                elapsed_ms = (end - start) * 1000
                hit_timings.append(elapsed_ms)

                print(
                    f"Cache HIT Request {i + 1}: "
                    f"{elapsed_ms:.2f} ms"
                )

        print("\n========== OPTIMIZED RESULTS ==========")

        print(f"Records: {TOTAL_RECORDS}")
        print(f"Cache MISS: {miss_timings[0]:.2f} ms")
        print(f"Cache HIT Average: {statistics.mean(hit_timings):.2f} ms")
        print(f"Cache HIT Minimum: {min(hit_timings):.2f} ms")
        print(f"Cache HIT Maximum: {max(hit_timings):.2f} ms")

        print("=======================================")
        print("\n========== SQL QUERY PROFILE ==========")

        print(f"Total SQL Queries: {query_count}")

        print(
            f"Total SQL Execution Time: "
            f"{sum(query_timings):.2f} ms"
        )

        if query_timings:
            print(
                f"Average SQL Query Time: "
                f"{statistics.mean(query_timings):.2f} ms"
            )

            print(
                f"Maximum SQL Query Time: "
                f"{max(query_timings):.2f} ms"
            )
        print("\n========== EXECUTED SQL STATEMENTS ==========")

        for index, statement in enumerate(query_statements, start=1):
            print(f"\nSQL Query {index}:")
            print(statement)

        print("=============================================")
        print("=======================================")
    finally:

        # Stop SQL query profiling
        event.remove(
            db.engine,
            "before_cursor_execute",
            before_cursor_execute
        )

        event.remove(
            db.engine,
            "after_cursor_execute",
            after_cursor_execute
        )

        print("SQL query profiling stopped.")

        print("\nCleaning benchmark data...")

        # Always rollback any failed or pending transaction first
        db.session.rollback()

        if benchmark_user_id is not None:
            cache.delete(f"analytics:user:{benchmark_user_id}")

            try:
                # Find all applications belonging to benchmark user
                application_subquery = (
                    db.session.query(JobApplication.id)
                    .filter_by(user_id=benchmark_user_id)
                )

                # Delete related history records first
                history_count = (
                    db.session.query(ApplicationStatusHistory)
                    .filter(
                        ApplicationStatusHistory.application_id.in_(
                            application_subquery
                        )
                    )
                    .delete(synchronize_session=False)
                )

                # Delete benchmark applications
                application_count = (
                    JobApplication.query
                    .filter_by(user_id=benchmark_user_id)
                    .delete(synchronize_session=False)
                )

                # Delete benchmark user
                benchmark_user = User.query.filter_by(
                    id=benchmark_user_id
                ).first()

                if benchmark_user:
                    db.session.delete(benchmark_user)

                db.session.commit()

                print("Benchmark cleanup completed.")
                print(f"Applications removed: {application_count}")
                print(f"History records removed: {history_count}")
                print(f"Benchmark user removed: {benchmark_user_id}")

            except Exception:
                db.session.rollback()
                raise

        else:
            print("No benchmark user created. Nothing to clean.")
