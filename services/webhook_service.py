
import hashlib
import hmac
import json
import logging
import os

from datetime import datetime, timedelta

import requests


logger = logging.getLogger(__name__)

MAX_WEBHOOK_RETRIES = 3
WEBHOOK_TIMEOUT = 5


def generate_webhook_signature(payload, secret):
    """Generate HMAC-SHA256 signature for webhook payload."""

    body = json.dumps(
        payload,
        separators=(",", ":"),
        sort_keys=True
    ).encode("utf-8")

    signature = hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()

    return body, f"sha256={signature}"


def verify_webhook_signature(payload_body, signature, secret):
    """Verify an incoming webhook HMAC signature."""

    if not isinstance(signature, str):
        return False

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload_body,
        hashlib.sha256
    ).hexdigest()

    expected_header = f"sha256={expected_signature}"

    return hmac.compare_digest(
        expected_header,
        signature
    )


def queue_application_status_change(
    db,
    WebhookDelivery,
    application,
    old_status,
    new_status
):
    """Queue outbound webhook and optional Slack notification."""

    if old_status == new_status:
        return 0

    payload = {
        "event": "application.status_changed",
        "application": {
            "id": application.id,
            "company": application.company,
            "role": application.role,
            "old_status": old_status.value,
            "new_status": new_status.value
        },
        "created_at": datetime.utcnow().isoformat()
    }

    deliveries_created = 0

    # Queue general outbound webhook
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        delivery = WebhookDelivery(
            event_type="application.status_changed",
            payload=payload,
            target_url=webhook_url,
            status="PENDING",
            attempt_count=0
        )

        db.session.add(delivery)
        deliveries_created += 1

    # Queue Slack notification only when status becomes OFFER
    if new_status.value == "OFFER":

        slack_url = os.getenv("SLACK_WEBHOOK_URL")

        if slack_url:
            slack_payload = {
                "text": (
                    ":tada: Job Offer Received!\n"
                    f"Company: {application.company}\n"
                    f"Role: {application.role}\n"
                    f"Status: {new_status.value}"
                )
            }

            slack_delivery = WebhookDelivery(
                event_type="slack.offer_notification",
                payload=slack_payload,
                target_url=slack_url,
                status="PENDING",
                attempt_count=0
            )

            db.session.add(slack_delivery)
            deliveries_created += 1

            logger.info(
                "Slack offer notification queued for application ID %s",
                application.id
            )

    return deliveries_created


def deliver_pending_webhooks():
    """
    Process pending webhook deliveries.

    Initial attempt + maximum 3 retries = 4 attempts.
    Must run inside Flask application context.
    """

    from app import db, WebhookDelivery

    now = datetime.utcnow()

    deliveries = WebhookDelivery.query.filter(
        WebhookDelivery.status == "PENDING",
        db.or_(
            WebhookDelivery.next_retry_at.is_(None),
            WebhookDelivery.next_retry_at <= now
        ),
        WebhookDelivery.attempt_count < MAX_WEBHOOK_RETRIES + 1
    ).order_by(
        WebhookDelivery.created_at.asc()
    ).limit(50).all()

    for delivery in deliveries:

        delivery_id = delivery.id
        event_type = delivery.event_type

        try:
            # Mark delivery as processing
            delivery.attempt_count += 1
            delivery.status = "PROCESSING"

            db.session.commit()

            headers = {
                "Content-Type": "application/json"
            }

            body, _ = generate_webhook_signature(
                delivery.payload,
                "temporary"
            )

            # Sign application webhooks, not Slack requests
            if event_type != "slack.offer_notification":

                secret = os.getenv("WEBHOOK_SECRET")

                if not secret:
                    raise ValueError(
                        "WEBHOOK_SECRET is not configured"
                    )

                body, signature = generate_webhook_signature(
                    delivery.payload,
                    secret
                )

                headers["X-Webhook-Signature"] = signature

            response = requests.post(
                delivery.target_url,
                data=body,
                headers=headers,
                timeout=WEBHOOK_TIMEOUT
            )

            response.raise_for_status()

            delivery.status = "DELIVERED"
            delivery.delivered_at = datetime.utcnow()
            delivery.next_retry_at = None
            delivery.last_error = None

            db.session.commit()

            logger.info(
                "Webhook delivery successful: ID %s, event %s",
                delivery_id,
                event_type
            )

        except Exception as error:

            db.session.rollback()

            delivery = db.session.get(
                WebhookDelivery,
                delivery_id
            )

            if delivery is None:
                logger.error(
                    "Webhook delivery record not found: ID %s",
                    delivery_id
                )
                continue

            delivery.last_error = str(error)[:1000]

            if delivery.attempt_count <= MAX_WEBHOOK_RETRIES:

                # Retry after 2, 4 and 8 seconds
                retry_delay = 2 ** delivery.attempt_count

                delivery.status = "PENDING"
                delivery.next_retry_at = (
                    datetime.utcnow()
                    + timedelta(seconds=retry_delay)
                )

            else:
                delivery.status = "FAILED"
                delivery.next_retry_at = None

            db.session.commit()

            logger.warning(
                "Webhook delivery failed: ID %s, attempt %s, status %s",
                delivery_id,
                delivery.attempt_count,
                delivery.status
            )
