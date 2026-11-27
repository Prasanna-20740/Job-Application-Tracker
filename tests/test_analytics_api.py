
from datetime import date, datetime, timedelta
from unittest.mock import patch

from app import (
    ApplicationStatus,
    ApplicationStatusHistory,
    JobApplication,
    cache,
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

    cache.delete(f"analytics:user:{auth_user.id}")

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


def test_application_analytics_cache_hit(client):
    cached_data = {
        "total_applications": 10,
        "response_rate": 50.0,
        "average_days_per_status": {},
        "best_day_to_apply": "Monday",
        "weekday_application_counts": {},
        "status_distribution": {},
    }

    with patch(
        "app.cache.get",
        return_value=cached_data
    ) as mock_cache_get:

        with patch("app.cache.set") as mock_cache_set:
            response = client.get("/api/analytics")

    assert response.status_code == 200
    assert response.json == cached_data

    # Cache should be checked once
    mock_cache_get.assert_called_once()

    # Cache HIT should not write to cache again
    mock_cache_set.assert_not_called()
def test_application_analytics_cache_miss_stores_result(
    client,
    auth_user
):
    expected_cache_key = f"analytics:user:{auth_user.id}"

    with patch(
        "app.cache.get",
        return_value=None
    ) as mock_cache_get:

        with patch("app.cache.set") as mock_cache_set:
            response = client.get("/api/analytics")

    # API should return successfully
    assert response.status_code == 200

    # Cache should be checked with the logged-in user's key
    mock_cache_get.assert_called_once_with(expected_cache_key)

    # Cache should store the calculated analytics
    mock_cache_set.assert_called_once()

    args, kwargs = mock_cache_set.call_args

    assert args[0] == expected_cache_key
    assert args[1]["total_applications"] == 0
    assert kwargs["timeout"] == 300