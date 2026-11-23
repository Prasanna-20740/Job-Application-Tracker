
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()


def check_upcoming_interviews():
    from app import db, Interview
    from services.email_service import send_interview_reminder

    now = datetime.utcnow()

    # Reminder window: approximately 24 hours before interview
    reminder_start = now + timedelta(hours=24) - timedelta(minutes=5)
    reminder_end = now + timedelta(hours=24)

    with scheduler.app.app_context():

        interviews = Interview.query.filter(
            Interview.interview_date > reminder_start,
            Interview.interview_date <= reminder_end,
            Interview.reminder_sent.is_(False)
        ).all()

        for interview in interviews:
            try:
                send_interview_reminder(interview)

            except Exception:
                db.session.rollback()

                scheduler.app.logger.exception(
                    "Failed to send reminder for interview ID %s",
                    interview.id
                )


def run_weekly_digest():
    from services.email_service import send_all_weekly_digests

    with scheduler.app.app_context():
        results = send_all_weekly_digests()

        scheduler.app.logger.info(
            "Weekly digest completed: %s",
            results
        )


def process_webhook_deliveries():
    """Process queued outbound webhooks and Slack notifications."""

    from services.webhook_service import deliver_pending_webhooks

    with scheduler.app.app_context():
        try:
            deliver_pending_webhooks()

        except Exception:
            from app import db

            db.session.rollback()

            scheduler.app.logger.exception(
                "Webhook delivery worker failed"
            )


def start_scheduler(app):
    scheduler.app = app

    if not scheduler.running:

        # Check interview reminders every 5 minutes
        scheduler.add_job(
            id="interview_reminder_job",
            func=check_upcoming_interviews,
            trigger="interval",
            minutes=5,
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

        # Send weekly digest every Monday at 9 AM
        scheduler.add_job(
            id="weekly_digest_job",
            func=run_weekly_digest,
            trigger="cron",
            day_of_week="mon",
            hour=9,
            minute=0,
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

        # Process pending webhooks every 1 second
        scheduler.add_job(
            id="webhook_delivery_job",
            func=process_webhook_deliveries,
            trigger="interval",
            seconds=1,
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

        scheduler.start()

        app.logger.info(
            "Interview, weekly digest and webhook schedulers started"
        )
