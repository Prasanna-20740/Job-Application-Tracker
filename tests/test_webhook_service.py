
from unittest.mock import Mock

from app import (
    db,
    WebhookDelivery,
    ApplicationStatus,
)

from services.webhook_service import (
    generate_webhook_signature,
    verify_webhook_signature,
    queue_application_status_change,
    deliver_pending_webhooks,
)


# -------------------------------------------------
# 1. HMAC signature tests
# -------------------------------------------------

def test_generate_webhook_signature():

    payload = {
        "event": "application.status_changed",
        "application_id": 1,
    }

    body, signature = generate_webhook_signature(
        payload,
        "test-secret"
    )

    assert isinstance(body, bytes)
    assert signature.startswith("sha256=")


def test_verify_valid_webhook_signature():

    payload = {"event": "test"}

    body, signature = generate_webhook_signature(
        payload,
        "test-secret"
    )

    assert verify_webhook_signature(
        body,
        signature,
        "test-secret"
    ) is True


def test_reject_invalid_webhook_signature():

    body = b'{"event":"test"}'

    assert verify_webhook_signature(
        body,
        "sha256=invalid",
        "test-secret"
    ) is False


def test_reject_missing_webhook_signature():

    assert verify_webhook_signature(
        b'{"event":"test"}',
        None,
        "test-secret"
    ) is False


# -------------------------------------------------
# 2. Webhook queue tests
# -------------------------------------------------

def test_queue_application_status_change(
    app,
    db,
    factories,
    monkeypatch
):

    monkeypatch.setenv(
        "WEBHOOK_URL",
        "https://example.com/webhook"
    )

    monkeypatch.delenv(
        "SLACK_WEBHOOK_URL",
        raising=False
    )

    application = factories["application"].create()

    db.session.flush()

    count = queue_application_status_change(
        db,
        WebhookDelivery,
        application,
        ApplicationStatus.APPLIED,
        ApplicationStatus.INTERVIEW
    )

    db.session.commit()

    delivery = WebhookDelivery.query.one()

    assert count == 1
    assert delivery.event_type == "application.status_changed"
    assert delivery.status == "PENDING"
    assert delivery.attempt_count == 0


def test_no_webhook_when_status_is_unchanged(
    app,
    db,
    factories,
    monkeypatch
):

    monkeypatch.setenv(
        "WEBHOOK_URL",
        "https://example.com/webhook"
    )

    application = factories["application"].create()

    db.session.flush()

    count = queue_application_status_change(
        db,
        WebhookDelivery,
        application,
        ApplicationStatus.APPLIED,
        ApplicationStatus.APPLIED
    )

    assert count == 0
    assert WebhookDelivery.query.count() == 0


# -------------------------------------------------
# 3. Slack notification test
# -------------------------------------------------

def test_queue_slack_offer_notification(
    app,
    db,
    factories,
    monkeypatch
):

    monkeypatch.delenv(
        "WEBHOOK_URL",
        raising=False
    )

    monkeypatch.setenv(
        "SLACK_WEBHOOK_URL",
        "https://hooks.slack.com/services/test"
    )

    application = factories["application"].create()

    db.session.flush()

    count = queue_application_status_change(
        db,
        WebhookDelivery,
        application,
        ApplicationStatus.APPLIED,
        ApplicationStatus.OFFER
    )

    db.session.commit()

    delivery = WebhookDelivery.query.one()

    assert count == 1
    assert delivery.event_type == "slack.offer_notification"
    assert delivery.status == "PENDING"
    assert "Job Offer Received!" in delivery.payload["text"]


# -------------------------------------------------
# 4. Successful delivery test
# -------------------------------------------------

def test_successful_webhook_delivery(
    app,
    db,
    factories,
    monkeypatch
):

    monkeypatch.setenv(
        "WEBHOOK_URL",
        "https://example.com/webhook"
    )

    monkeypatch.setenv(
        "WEBHOOK_SECRET",
        "test-secret"
    )

    monkeypatch.delenv(
        "SLACK_WEBHOOK_URL",
        raising=False
    )

    application = factories["application"].create()

    db.session.flush()

    queue_application_status_change(
        db,
        WebhookDelivery,
        application,
        ApplicationStatus.APPLIED,
        ApplicationStatus.INTERVIEW
    )

    db.session.commit()

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None

    mock_post = Mock(return_value=mock_response)

    monkeypatch.setattr(
        "services.webhook_service.requests.post",
        mock_post
    )

    with app.app_context():
        deliver_pending_webhooks()

    delivery = WebhookDelivery.query.one()

    assert mock_post.called
    assert delivery.status == "DELIVERED"
    assert delivery.attempt_count == 1
    assert delivery.delivered_at is not None


# -------------------------------------------------
# 5. Failed delivery and retry test
# -------------------------------------------------

def test_failed_webhook_delivery_schedules_retry(
    app,
    db,
    factories,
    monkeypatch
):

    monkeypatch.setenv(
        "WEBHOOK_URL",
        "https://example.com/webhook"
    )

    monkeypatch.setenv(
        "WEBHOOK_SECRET",
        "test-secret"
    )

    monkeypatch.delenv(
        "SLACK_WEBHOOK_URL",
        raising=False
    )

    application = factories["application"].create()

    db.session.flush()

    queue_application_status_change(
        db,
        WebhookDelivery,
        application,
        ApplicationStatus.APPLIED,
        ApplicationStatus.INTERVIEW
    )

    db.session.commit()

    mock_post = Mock(
        side_effect=Exception("Connection failed")
    )

    monkeypatch.setattr(
        "services.webhook_service.requests.post",
        mock_post
    )

    # Prevent rollback from removing the test delivery record
    monkeypatch.setattr(
        db.session,
        "rollback",
        lambda: None
    )

    with app.app_context():
        deliver_pending_webhooks()

    delivery = WebhookDelivery.query.one()

    assert mock_post.called
    assert delivery.status == "PENDING"
    assert delivery.attempt_count == 1
    assert delivery.next_retry_at is not None
    assert "Connection failed" in delivery.last_error



def test_webhook_marked_failed_after_max_retries(
    app,
    db,
    factories,
    monkeypatch
):

    monkeypatch.setenv(
        "WEBHOOK_SECRET",
        "test-secret"
    )

    application = factories["application"].create()

    db.session.flush()

    delivery = WebhookDelivery(
        event_type="application.status_changed",
        payload={"event": "test"},
        target_url="https://example.com/webhook",
        status="PENDING",
        attempt_count=3
    )

    db.session.add(delivery)
    db.session.commit()

    mock_post = Mock(
        side_effect=Exception("Connection failed")
    )

    monkeypatch.setattr(
        "services.webhook_service.requests.post",
        mock_post
    )

    monkeypatch.setattr(
        db.session,
        "rollback",
        lambda: None
    )

    with app.app_context():
        deliver_pending_webhooks()

    delivery = WebhookDelivery.query.one()

    assert delivery.status == "FAILED"
    assert delivery.attempt_count == 4
    assert delivery.next_retry_at is None
    assert "Connection failed" in delivery.last_error
