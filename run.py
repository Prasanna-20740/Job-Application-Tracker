import os

from app import app
from services.scheduler_service import start_scheduler


if __name__ == "__main__":

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler(app)

    app.run(debug=True)