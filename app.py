from datetime import date
from enum import Enum
import logging
import os
import re
import uuid

from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory
)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

# --------------------------------------------------
# Logger Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    force=True
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Flask Configuration
# --------------------------------------------------

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path, "uploads"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres123@localhost:5434/job_tracker"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# --------------------------------------------------
# Application Status Enum
# --------------------------------------------------

class ApplicationStatus(Enum):
    APPLIED = "APPLIED"
    PHONE_SCREEN = "PHONE_SCREEN"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"


# --------------------------------------------------
# User Model
# --------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


# --------------------------------------------------
# Job Application Model
# --------------------------------------------------

class JobApplication(db.Model):
    __tablename__ = "job_application"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(
        db.String(150),
        nullable=False
    )

    role = db.Column(
        db.String(150),
        nullable=False
    )

    status = db.Column(
        db.Enum(
            ApplicationStatus,
            name="application_status"
        ),
        nullable=False,
        default=ApplicationStatus.APPLIED
    )

    applied_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    # Resume file path
    resume_path = db.Column(
        db.String(255),
        nullable=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "status": self.status.value,
            "applied_date": (
                self.applied_date.isoformat()
                if self.applied_date else None
            ),
            "notes": self.notes,
            "user_id": self.user_id,
            "resume_path": self.resume_path
        }


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def is_valid_user_id(user_id):

    if user_id is None:
        return True

    if not isinstance(user_id, int) or isinstance(user_id, bool):
        return False

    return db.session.get(User, user_id) is not None


def parse_application_data(data, creating=False):

    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")

    parsed = {}

    # Company validation
    if creating and "company" not in data:
        raise ValueError("Company is required")

    if "company" in data:
        company = data["company"]

        if not isinstance(company, str) or not company.strip():
            raise ValueError("Company must be a non-empty string")

        parsed["company"] = company.strip()

    # Role validation
    if creating and "role" not in data:
        raise ValueError("Role is required")

    if "role" in data:
        role = data["role"]

        if not isinstance(role, str) or not role.strip():
            raise ValueError("Role must be a non-empty string")

        parsed["role"] = role.strip()

    # Notes validation
    if "notes" in data:
        notes = data["notes"]

        if notes is not None and not isinstance(notes, str):
            raise ValueError("Notes must be a string or null")

        parsed["notes"] = (
            notes.strip() if isinstance(notes, str) else None
        )

    # Status validation
    if "status" in data:
        status = data["status"]

        if not isinstance(status, str):
            raise ValueError("Status must be a string")

        try:
            parsed["status"] = ApplicationStatus(
                status.strip().upper()
            ).value

        except ValueError:
            valid_statuses = [
                item.value for item in ApplicationStatus
            ]

            raise ValueError(
                f"Invalid status. Allowed values: {valid_statuses}"
            )

    # Applied date validation
    if "applied_date" in data:
        applied_date = data["applied_date"]

        if not isinstance(applied_date, str):
            raise ValueError(
                "applied_date must use YYYY-MM-DD format"
            )

        try:
            parsed["applied_date"] = date.fromisoformat(applied_date)

        except ValueError:
            raise ValueError(
                "Invalid applied_date. Use YYYY-MM-DD format"
            )

    # User ID validation
    if "user_id" in data:
        user_id = data["user_id"]

        if user_id is not None and not is_valid_user_id(user_id):
            raise ValueError("Invalid user_id")

        parsed["user_id"] = user_id

    return parsed


# --------------------------------------------------
# Resume Helper Functions
# --------------------------------------------------

def delete_resume_file(resume_path):

    if not resume_path:
        return

    # Only delete files inside the configured uploads folder
    filename = os.path.basename(resume_path)

    if not filename:
        return

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info("Resume file deleted: %s", filename)

    except OSError:
        logger.exception("Unable to delete resume file: %s", filename)


def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    if reader.is_encrypted:
        raise ValueError("Password-protected PDFs are not supported")

    extracted_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text.append(page_text)

    return "\n".join(extracted_text)


def extract_skills(text):

    skills_list = [
        "Python",
        "Flask",
        "Django",
        "Java",
        "JavaScript",
        "React",
        "HTML",
        "CSS",
        "SQL",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Docker",
        "Git",
        "GitHub",
        "REST API",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "AWS"
    ]

    found_skills = []

    for skill in skills_list:
        pattern = (
            r"(?<!\w)" +
            re.escape(skill) +
            r"(?!\w)"
        )

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# --------------------------------------------------
# Application Service Layer
# --------------------------------------------------

from services.application_service import (
    ApplicationService,
    ApplicationNotFound,
    DuplicateApplication
)

application_service = ApplicationService(
    db,
    JobApplication,
    ApplicationStatus
)


# --------------------------------------------------
# Home API
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Job Application Tracker API is running"
    }), 200


# --------------------------------------------------
# Create User API
# --------------------------------------------------

@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Valid JSON object is required"
        }), 400

    username = data.get("username")
    email = data.get("email")

    if not isinstance(username, str) or not username.strip():
        return jsonify({
            "error": "Username is required"
        }), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "error": "Email is required"
        }), 400

    username = username.strip()
    email = email.strip()

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return jsonify({
            "error": "Username or email already exists"
        }), 409

    try:
        user = User(
            username=username,
            email=email
        )

        db.session.add(user)
        db.session.commit()

        logger.info("User created successfully: ID %s", user.id)

        return jsonify({
            "message": "User created successfully",
            "user": user.to_dict()
        }), 201

    except Exception:
        db.session.rollback()
        logger.exception("Error creating user")

        return jsonify({
            "error": "Failed to create user"
        }), 500


# --------------------------------------------------
# Get All Users API
# --------------------------------------------------

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.order_by(User.id).all()

    logger.info("Retrieved %s users", len(users))

    return jsonify([
        user.to_dict() for user in users
    ]), 200


# --------------------------------------------------
# Get All Applications API
# --------------------------------------------------

@app.route("/applications", methods=["GET"])
def get_applications():

    try:
        applications = application_service.list_applications()

        return jsonify([
            application.to_dict()
            for application in applications
        ]), 200

    except Exception:
        logger.exception("Error retrieving applications")

        return jsonify({
            "error": "Internal server error"
        }), 500


# --------------------------------------------------
# Create Application API
# --------------------------------------------------

@app.route("/applications", methods=["POST"])
def create_application():

    data = request.get_json(silent=True)

    try:
        parsed = parse_application_data(
            data,
            creating=True
        )

        application = application_service.create_application(
            company=parsed["company"],
            role=parsed["role"],
            status=parsed.get("status", "APPLIED"),
            notes=parsed.get("notes"),
            applied_date=parsed.get("applied_date"),
            user_id=parsed.get("user_id")
        )

        return jsonify({
            "message": "Application created successfully",
            "application": application.to_dict()
        }), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except DuplicateApplication as error:
        return jsonify({"error": str(error)}), 409

    except Exception:
        logger.exception("Error creating application")

        return jsonify({
            "error": "Internal server error"
        }), 500


# --------------------------------------------------
# Get Application By ID API
# --------------------------------------------------

@app.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):

    try:
        application = application_service.get_application(
            application_id
        )

        return jsonify(application.to_dict()), 200

    except ApplicationNotFound as error:
        return jsonify({"error": str(error)}), 404

    except Exception:
        logger.exception("Error retrieving application")

        return jsonify({
            "error": "Internal server error"
        }), 500


# --------------------------------------------------
# Update Application API
# --------------------------------------------------

@app.route("/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):

    data = request.get_json(silent=True)

    try:
        parsed = parse_application_data(data)

        if not parsed:
            return jsonify({
                "error": "At least one field is required"
            }), 400

        application = application_service.update_application(
            application_id,
            parsed
        )

        return jsonify({
            "message": "Application updated successfully",
            "application": application.to_dict()
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except ApplicationNotFound as error:
        return jsonify({"error": str(error)}), 404

    except DuplicateApplication as error:
        return jsonify({"error": str(error)}), 409

    except Exception:
        logger.exception("Error updating application")

        return jsonify({
            "error": "Internal server error"
        }), 500


# --------------------------------------------------
# Delete Application API
# --------------------------------------------------

@app.route("/applications/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):

    try:
        application = application_service.get_application(
            application_id
        )

        resume_path = application.resume_path

        deleted_application = application_service.delete_application(
            application_id
        )

        # Delete physical resume after database deletion succeeds
        delete_resume_file(resume_path)

        return jsonify({
            "message": "Application deleted successfully",
            "application": deleted_application.to_dict()
        }), 200

    except ApplicationNotFound as error:
        return jsonify({"error": str(error)}), 404

    except Exception:
        logger.exception("Error deleting application")

        return jsonify({
            "error": "Internal server error"
        }), 500


# --------------------------------------------------
# Upload Resume API
# --------------------------------------------------

@app.route(
    "/applications/<int:application_id>/resume",
    methods=["POST"]
)
def upload_resume(application_id):

    try:
        application = application_service.get_application(
            application_id
        )

        if "resume" not in request.files:
            return jsonify({
                "error": "Resume file is required"
            }), 400

        file = request.files["resume"]

        if not file.filename:
            return jsonify({
                "error": "No file selected"
            }), 400

        original_filename = secure_filename(file.filename)

        if not original_filename.lower().endswith(".pdf"):
            return jsonify({
                "error": "Only PDF files are allowed"
            }), 400

        # Check actual PDF signature
        file_signature = file.stream.read(4)
        file.stream.seek(0)

        if file_signature != b"%PDF":
            return jsonify({
                "error": "Invalid PDF file"
            }), 400

        unique_filename = (
            f"{uuid.uuid4().hex}_{original_filename}"
        )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        # Save the uploaded file
        file.save(file_path)

        old_resume_path = application.resume_path

        # Store relative path in database
        application.resume_path = os.path.join(
            f"uploads/{unique_filename}"
        )

        try:
            db.session.commit()

        except Exception:
            db.session.rollback()

            if os.path.isfile(file_path):
                os.remove(file_path)

            raise

        # Remove previous resume after successful update
        delete_resume_file(old_resume_path)

        logger.info(
            "Resume uploaded for application ID %s",
            application_id
        )

        return jsonify({
            "message": "Resume uploaded successfully",
            "application_id": application_id,
            "resume_path": application.resume_path,
            "file_url": (
                f"/files/{application.resume_path}"
            )
        }), 201

    except ApplicationNotFound as error:
        return jsonify({"error": str(error)}), 404

    except Exception:
        db.session.rollback()
        logger.exception("Error uploading resume")

        return jsonify({
            "error": "Failed to upload resume"
        }), 500


# --------------------------------------------------
# Serve Uploaded Resume API
# --------------------------------------------------

@app.route("/files/<path:filename>", methods=["GET"])
def serve_resume(filename):

    try:
        return send_from_directory(
            app.root_path,
            filename,
            as_attachment=False
        )

    except Exception:
        logger.exception("Error serving resume")

        return jsonify({
            "error": "Resume file not found"
        }), 404


# --------------------------------------------------
# Extract Resume Skills API
# --------------------------------------------------

@app.route(
    "/applications/<int:application_id>/resume/skills",
    methods=["GET"]
)
def get_resume_skills(application_id):

    try:
        application = application_service.get_application(
            application_id
        )

        if not application.resume_path:
            return jsonify({
                "error": "No resume uploaded for this application"
            }), 404

        filename = os.path.basename(application.resume_path)

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        if not os.path.isfile(file_path):
            return jsonify({
                "error": "Resume file not found"
            }), 404

        extracted_text = extract_pdf_text(file_path)

        skills = extract_skills(extracted_text)

        return jsonify({
            "application_id": application_id,
            "extracted_text": extracted_text,
            "skills": skills
        }), 200

    except ApplicationNotFound as error:
        return jsonify({"error": str(error)}), 404

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        logger.exception("Error extracting resume skills")

        return jsonify({
            "error": "Failed to extract resume text"
        }), 500


# --------------------------------------------------
# File Size Error Handler
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "error": "File size exceeds the 5 MB limit"
    }), 413


# --------------------------------------------------
# Run Flask Application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)