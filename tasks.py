import logging
import os
from datetime import datetime, timedelta

from flask_mail import Message

from celery_app import celery
from app import (
    app as flask_app,
    db,
    mail,
    User,
    JobApplication,
    ApplicationStatus,
    extract_pdf_text,
    extract_skills
)


logger = logging.getLogger(__name__)


# --------------------------------------------------
# Asynchronous Resume Parsing Task
# --------------------------------------------------

@celery.task(
    bind=True,
    name="tasks.parse_resume"
)
def parse_resume_task(self, application_id):

    application = JobApplication.query.get(application_id)

    if application is None:
        return {
            "status": "NOT_FOUND",
            "application_id": application_id
        }

    if not application.resume_path:
        application.resume_parse_status = "FAILED"
        db.session.commit()

        return {
            "status": "FAILED",
            "message": "No resume file found",
            "application_id": application_id
        }

    upload_folder = flask_app.config.get(
        "UPLOAD_FOLDER",
        os.path.join(flask_app.root_path, "uploads")
    )

    file_path = os.path.join(
        upload_folder,
        os.path.basename(application.resume_path)
    )

    try:

        # Mark parsing as started.
        application.resume_parse_status = "PROCESSING"
        db.session.commit()

        if not os.path.isfile(file_path):
            raise FileNotFoundError("Resume file not found")

        # Extract PDF text.
        extracted_text = extract_pdf_text(file_path)

        # Extract skills from resume text.
        skills = extract_skills(extracted_text)

        # Save parsing results.
        application.resume_text = extracted_text
        application.resume_skills = skills
        application.resume_parse_status = "COMPLETED"
        application.resume_parsed_at = datetime.utcnow()

        db.session.commit()

        logger.info(
            "Resume parsing completed for application %s",
            application_id
        )

        return {
            "status": "COMPLETED",
            "application_id": application_id,
            "skills": skills
        }

    except Exception:

        db.session.rollback()

        logger.exception(
            "Resume parsing failed for application %s",
            application_id
        )

        # Update the database status after failure.
        application = JobApplication.query.get(application_id)

        if application is not None:
            application.resume_parse_status = "FAILED"
            db.session.commit()

        raise

# --------------------------------------------------
# Stale Application Alert - Day 16
# --------------------------------------------------

@celery.task(
    bind=True,
    name="tasks.send_stale_application_alerts"
)
def send_stale_application_alerts(self):

    cutoff_date = datetime.utcnow() - timedelta(days=14)

    stale_applications = JobApplication.query.filter(
        JobApplication.updated_at <= cutoff_date,
        JobApplication.stale_alert_sent_at.is_(None),
        JobApplication.user_id.isnot(None),
        JobApplication.status.notin_([
            ApplicationStatus.OFFER,
            ApplicationStatus.REJECTED
        ])
    ).all()

    sent_count = 0
    failed_count = 0

    for application in stale_applications:

        try:
            user = application.user

            if user is None or not user.email:
                logger.warning(
                    "No email found for application %s",
                    application.id
                )
                continue

            message = Message(
                subject="Reminder: Update Your Job Application",
                recipients=[user.email],
                body=(
                    f"Hello {user.username},\n\n"
                    f"Your job application for "
                    f"{application.role} at {application.company} "
                    f"has not been updated for more than 14 days.\n\n"
                    "Please log in to your Job Application Tracker "
                    "and update its current status.\n\n"
                    "Regards,\n"
                    "Job Application Tracker"
                )
            )

            mail.send(message)

            application.stale_alert_sent_at = datetime.utcnow()
            db.session.commit()

            sent_count += 1

            logger.info(
                "Stale alert sent for application %s",
                application.id
            )

        except Exception:

            db.session.rollback()
            failed_count += 1

            logger.exception(
                "Failed to send stale alert for application %s",
                application.id
            )

    return {
        "status": "COMPLETED",
        "total_stale": len(stale_applications),
        "sent": sent_count,
        "failed": failed_count
    }
