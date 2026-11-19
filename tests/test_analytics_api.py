from datetime import date, datetime, timedelta

from app import (
    ApplicationStatus,
    ApplicationStatusHistory,
)


def test_application_analytics(client, auth_user, db):
    today = date.today()

    # Create 4 applications with different statuses and dates
    applications_data = [
        (ApplicationStatus.APPLIED, today - timedelta(days=3)),
        (ApplicationStatus.INTERVIEW, today - timedelta(days=7)),
        (ApplicationStatus.INTERVIEW, today - timedelta(days=7)),
        (ApplicationStatus.REJECTED, today - timedelta(days=14)),
    ]

    for status, applied_date in applications_data:
        from app import JobApplication

        application = JobApplication(
            company=f"Company {status.value}",
            role="Developer",
            status=status,
            applied_date=applied_date,
            user_id=auth_user.id,
        )

        db.session.add(application)
        db.session.flush()

        db.session.add(
            ApplicationStatusHistory(
                application_id=application.id,
                status=status,
                entered_at=datetime.utcnow() - timedelta(days=2),
                exited_at=datetime.utcnow(),
            )
        )

    db.session.commit()

    response = client.get("/api/analytics")

    assert response.status_code == 200

    data = response.json

    assert data["total_applications"] == 4
    assert data["response_rate"] == 50.0

    assert data["status_distribution"] == {
        "APPLIED": 1,
        "PHONE_SCREEN": 0,
        "INTERVIEW": 2,
        "OFFER": 0,
        "REJECTED": 1,
    }

    assert data["average_days_per_status"]["APPLIED"] == 2.0
    assert data["average_days_per_status"]["INTERVIEW"] == 2.0
    assert data["average_days_per_status"]["REJECTED"] == 2.0

    assert data["best_day_to_apply"] == (
        today - timedelta(days=7)
    ).strftime("%A")