import os

from celery import Celery
from celery.schedules import crontab

from app import app as flask_app


# --------------------------------------------------
# Celery Configuration
# --------------------------------------------------

celery = Celery(
    "job_application_tracker",
    broker=os.getenv(
        "CELERY_BROKER_URL",
        "redis://localhost:6379/2"
    ),
    backend=os.getenv(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379/3"
    )
)


# --------------------------------------------------
# Celery Settings
# --------------------------------------------------

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    timezone="Asia/Kolkata",
    enable_utc=True,

    task_track_started=True,
    result_expires=3600,

    broker_connection_retry_on_startup=True
)


# --------------------------------------------------
# Flask Application Context
# --------------------------------------------------

class FlaskContextTask(celery.Task):

    abstract = True

    def __call__(self, *args, **kwargs):

        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = FlaskContextTask

# --------------------------------------------------
# Celery Task Discovery
# --------------------------------------------------

celery.conf.imports = (
    "tasks",
)

# --------------------------------------------------
# Celery Beat - Periodic Tasks
# --------------------------------------------------

celery.conf.beat_schedule = {
    "daily-stale-application-alerts": {
        "task": "tasks.send_stale_application_alerts",
        "schedule": crontab(hour=9, minute=0),
    },
}