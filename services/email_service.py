
from datetime import datetime, timedelta, timezone

from flask import current_app, render_template
from flask_mail import Message

from app import db, mail, User, JobApplication


def send_weekly_digest(user):
    """
    Send a weekly digest containing applications
    updated during the last 7 days.
    """

    week_ago = datetime.now(timezone.utc).replace(
        tzinfo=None
    ) - timedelta(days=7)

    applications = (
        JobApplication.query
        .filter(
            JobApplication.user_id == user.id,
            JobApplication.updated_at >= week_ago
        )
        .order_by(JobApplication.updated_at.desc())
        .all()
    )

    html_content = render_template(
        "emails/weekly_digest.html",
        username=user.username,
        total_applications=len(applications),
        applications=applications
    )

    message = Message(
        subject="Your Weekly Job Application Digest",
        recipients=[user.email],
        html=html_content
    )

    mail.send(message)

    current_app.logger.info(
        "Weekly digest sent to %s", user.email
    )

    return len(applications)


def send_all_weekly_digests():
    """
    Send weekly digest emails to all registered users.
    """

    users = User.query.all()
    results = []

    for user in users:
        try:
            count = send_weekly_digest(user)

            results.append({
                "user_id": user.id,
                "email": user.email,
                "applications": count,
                "success": True
            })

        except Exception:
            current_app.logger.exception(
                "Failed to send weekly digest to %s",
                user.email
            )

            results.append({
                "user_id": user.id,
                "email": user.email,
                "success": False
            })

    return results


def send_interview_reminder(interview):
    """
    Send an email reminder for an upcoming interview.
    """

    application = interview.application
    user = application.user

    html_content = render_template(
        "emails/interview_reminder.html",
        username=user.username,
        company=application.company,
        role=application.role,
        interview_date=interview.interview_date.strftime("%d-%m-%Y"),
        interview_time=interview.interview_date.strftime("%I:%M %p")
    )

    message = Message(
        subject=f"Interview Reminder - {application.company}",
        recipients=[user.email],
        html=html_content
    )

    mail.send(message)

    interview.reminder_sent = True
    db.session.commit()

    current_app.logger.info(
        "Interview reminder sent to %s for %s",
        user.email,
        application.company
    )
