
from datetime import date, timedelta, datetime
from enum import Enum
import logging
import os
import re
import uuid
import csv
import io

from dotenv import load_dotenv
from flask_caching import Cache
from services.job_search_service import job_search_service
from schemas.job_suggestion import JobSuggestion
from flask_mail import Mail, Message
from functools import wraps

load_dotenv()

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    decode_token
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask import (
    jsonify,
    request,
    send_from_directory,
    Response
)

from flask_openapi3 import OpenAPI, Info
from pydantic import BaseModel, Field

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from schemas.application_schema import ApplicationSchema
from marshmallow import ValidationError

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

app = OpenAPI(
    __name__,
    info=Info(
        title="Job Application Tracker API",
        version="1.0.0",
        description="REST API for managing job applications"
    ),
    security_schemes={
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
)

security = [{"BearerAuth": []}]


# Redis Cache Configuration
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)
app.config["CACHE_DEFAULT_TIMEOUT"] = 1800

cache = Cache(app)


# Upload Configuration
app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path, "uploads"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres123@localhost:5434/job_tracker"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Email Configuration - Mailtrap SMTP

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 2525))
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
app.config["MAIL_DEFAULT_SENDER"] = os.getenv(
    "MAIL_DEFAULT_SENDER",
    "testing@example.com"
)

mail = Mail(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# --------------------------------------------------
# JWT Configuration
# --------------------------------------------------

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "local-development-secret-change-before-production"
)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

jwt = JWTManager(app)


# --------------------------------------------------
# Application Status Enum
# --------------------------------------------------

class ApplicationStatus(Enum):
    APPLIED = "APPLIED"
    PHONE_SCREEN = "PHONE_SCREEN"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

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

    password_hash = db.Column(
        db.String(255),
        nullable=True
    )

    role = db.Column(
    db.Enum(Role, name="user_role"),
    nullable=False,
    default=Role.USER
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
# Token Blocklist Model
# --------------------------------------------------

class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    jti = db.Column(
        db.String(36),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

# --------------------------------------------------
# Audit Log Model
# --------------------------------------------------

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    actor_user_id = db.Column(
        db.Integer,
        nullable=True
    )

    actor_username = db.Column(
        db.String(100),
        nullable=False
    )

    action = db.Column(
        db.String(100),
        nullable=False
    )

    target_user_id = db.Column(
        db.Integer,
        nullable=True
    )

    target_username = db.Column(
        db.String(100),
        nullable=True
    )

    details = db.Column(
        db.JSON,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


def record_audit(
    actor,
    action,
    target=None,
    details=None
):
    audit = AuditLog(
        actor_user_id=actor.id,
        actor_username=actor.username,
        action=action,
        target_user_id=target.id if target else None,
        target_username=target.username if target else None,
        details=details
    )

    db.session.add(audit)
  
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

    resume_path = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow
    )

    updated_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
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
# Interview Model
# --------------------------------------------------

class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("job_application.id"),
        nullable=False
    )

    interview_date = db.Column(
        db.DateTime,
        nullable=False
    )

    interview_type = db.Column(
        db.String(100),
        nullable=True
    )

    meeting_link = db.Column(
        db.String(500),
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    reminder_sent = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    application = db.relationship(
        "JobApplication",
        backref=db.backref("interviews", lazy=True)
    )

# --------------------------------------------------
# Application Status History Model
# --------------------------------------------------

class ApplicationStatusHistory(db.Model):
    __tablename__ = "application_status_history"

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("job_application.id"),
        nullable=False,
        index=True
    )

    status = db.Column(
        db.Enum(
            ApplicationStatus,
            name="application_history_status"
        ),
        nullable=False
    )

    entered_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    exited_at = db.Column(
        db.DateTime,
        nullable=True
    )

    application = db.relationship(
        "JobApplication",
        backref=db.backref("status_history", lazy=True)
    )
 

# --------------------------------------------------
# Webhook Delivery Model
# --------------------------------------------------

class WebhookDelivery(db.Model):
    __tablename__ = "webhook_deliveries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    event_type = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    payload = db.Column(
        db.JSON,
        nullable=False
    )

    target_url = db.Column(
        db.String(1000),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING",
        index=True
    )

    attempt_count = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    next_retry_at = db.Column(
        db.DateTime,
        nullable=True
    )

    last_error = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    delivered_at = db.Column(
        db.DateTime,
        nullable=True
    )


# --------------------------------------------------
# JWT Token Blocklist Callback
# --------------------------------------------------

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]

    token = db.session.query(TokenBlocklist.id).filter_by(
        jti=jti
    ).scalar()

    return token is not None
# --------------------------------------------------
# Admin Authorization Decorator
# --------------------------------------------------

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorated_function(*args, **kwargs):

        try:
            current_user_id = int(get_jwt_identity())
        except (TypeError, ValueError):
            return jsonify({
                "error": "Invalid user identity"
            }), 401

        current_user = db.session.get(User, current_user_id)

        if current_user is None:
            return jsonify({
                "error": "User not found"
            }), 404

        if current_user.role != Role.ADMIN:
            return jsonify({
                "error": "Admin access required"
            }), 403

        return fn(*args, **kwargs)

    return decorated_function

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

    if creating and "company" not in data:
        raise ValueError("Company is required")

    if "company" in data:
        company = data["company"]

        if not isinstance(company, str) or not company.strip():
            raise ValueError("Company must be a non-empty string")

        parsed["company"] = company.strip()

    if creating and "role" not in data:
        raise ValueError("Role is required")

    if "role" in data:
        role = data["role"]

        if not isinstance(role, str) or not role.strip():
            raise ValueError("Role must be a non-empty string")

        parsed["role"] = role.strip()

    if "notes" in data:
        notes = data["notes"]

        if notes is not None and not isinstance(notes, str):
            raise ValueError("Notes must be a string or null")

        parsed["notes"] = (
            notes.strip() if isinstance(notes, str) else None
        )

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
    ApplicationStatus,
    ApplicationStatusHistory,
    WebhookDelivery
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
# JWT Authentication APIs
# --------------------------------------------------

@app.route("/api/auth/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "error": "Username, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return jsonify({
            "error": "Username or email already exists"
        }), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


@app.route("/api/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.password_hash:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

@app.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    current_user_id = get_jwt_identity()

    new_access_token = create_access_token(
        identity=current_user_id
    )

    return jsonify({
        "message": "Access token refreshed successfully",
        "access_token": new_access_token
    }), 200

@app.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():

    try:
        current_user_id = str(get_jwt_identity())

        # Revoke access token
        access_jti = get_jwt()["jti"]

        access_blocked = TokenBlocklist.query.filter_by(
            jti=access_jti
        ).first()

        if access_blocked is None:
            db.session.add(
                TokenBlocklist(jti=access_jti)
            )

        db.session.commit()

        # Revoke refresh token if supplied
        data = request.get_json(silent=True) or {}
        refresh_token = data.get("refresh_token")

        if refresh_token:
            refresh_payload = decode_token(refresh_token)

            if (
                refresh_payload.get("type") != "refresh"
                or refresh_payload.get("sub") != current_user_id
            ):
                return jsonify({
                    "error": "Invalid refresh token"
                }), 400

            refresh_jti = refresh_payload["jti"]

            refresh_blocked = TokenBlocklist.query.filter_by(
                jti=refresh_jti
            ).first()

            if refresh_blocked is None:
                db.session.add(
                    TokenBlocklist(jti=refresh_jti)
                )

                db.session.commit()

        return jsonify({
            "message": "Logout successful. Access and refresh tokens revoked."
        }), 200

    except Exception:
        db.session.rollback()
        logger.exception("Error during logout")

        return jsonify({
            "error": "Logout failed"
        }), 500

class ApplicationQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)
    status: str | None = None
    
class ApplicationPath(BaseModel):
    application_id: int = Field(gt=0)
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)
    status: str | None = None


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "APPLIED"
    applied_date: date | None = None
    notes: str | None = None
    
# --------------------------------------------------
# Create User API
# --------------------------------------------------

@app.route("/users", methods=["POST"])
@jwt_required()
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
@admin_required
def get_users():

    users = User.query.order_by(User.id).all()

    logger.info("Retrieved %s users", len(users))

    return jsonify([
        user.to_dict() for user in users
    ]), 200


# --------------------------------------------------
# Admin Delete User API
# --------------------------------------------------

@app.route("/admin/users/<int:user_id>", methods=["DELETE"])
@admin_required
def admin_delete_user(user_id):

    try:
        # Get logged-in admin
        admin_id = int(get_jwt_identity())
        admin = db.session.get(User, admin_id)

        # Prevent admin from deleting own account
        if admin_id == user_id:
            return jsonify({
                "error": "You cannot delete your own account"
            }), 400

        # Find target user
        target_user = db.session.get(User, user_id)

        if target_user is None:
            return jsonify({
                "error": "User not found"
            }), 404

        # Prevent deletion of the last admin
        if target_user.role == Role.ADMIN:
            admin_count = User.query.filter_by(
                role=Role.ADMIN
            ).count()

            if admin_count <= 1:
                return jsonify({
                    "error": "Cannot delete the last admin"
                }), 400

        # Find target user's applications
        applications = JobApplication.query.filter_by(
            user_id=user_id
        ).all()

        application_ids = [
            application.id for application in applications
        ]

        # Delete related interviews and status history
        if application_ids:

            Interview.query.filter(
                Interview.application_id.in_(application_ids)
            ).delete(synchronize_session=False)

            ApplicationStatusHistory.query.filter(
                ApplicationStatusHistory.application_id.in_(
                    application_ids
                )
            ).delete(synchronize_session=False)

        # Delete applications
        for application in applications:
            db.session.delete(application)

        # Record audit log before deleting user
        record_audit(
            actor=admin,
            action="DELETE_USER",
            target=target_user,
            details={
                "deleted_applications": len(applications)
            }
        )

        # Delete user
        db.session.delete(target_user)

        db.session.commit()

        return jsonify({
            "message": "User deleted successfully",
            "deleted_user_id": user_id,
            "deleted_applications": len(applications)
        }), 200

    except Exception:
        db.session.rollback()
        logger.exception("Admin user deletion failed")

        return jsonify({
            "error": "Failed to delete user"
        }), 500


# --------------------------------------------------
# Admin Impersonate User API
# --------------------------------------------------

@app.route(
    "/admin/users/<int:user_id>/impersonate",
    methods=["POST"]
)
@admin_required
def admin_impersonate_user(user_id):

    try:
        # Get logged-in admin
        admin_id = int(get_jwt_identity())
        admin = db.session.get(User, admin_id)

        # Find target user
        target_user = db.session.get(User, user_id)

        if target_user is None:
            return jsonify({
                "error": "User not found"
            }), 404

        # Prevent impersonating another admin
        if target_user.role == Role.ADMIN:
            return jsonify({
                "error": "Cannot impersonate another admin"
            }), 403

        # Create access token for target user
        impersonation_token = create_access_token(
            identity=str(target_user.id),
            additional_claims={
                "is_impersonation": True,
                "impersonated_by": admin.id
            }
        )

        # Record audit log
        record_audit(
            actor=admin,
            action="IMPERSONATE_USER",
            target=target_user,
            details={
                "impersonation": True
            }
        )

        db.session.commit()

        return jsonify({
            "message": "User impersonation started",
            "access_token": impersonation_token,
            "user": target_user.to_dict(),
            "is_impersonation": True
        }), 200

    except Exception:
        db.session.rollback()
        logger.exception("Admin impersonation failed")

        return jsonify({
            "error": "Failed to impersonate user"
        }), 500

# --------------------------------------------------
# Get All Applications API (Paginated + Filterable)
# --------------------------------------------------

@app.get(
    "/applications",
    summary="Get all applications",
    description="Get paginated and filterable applications for the logged-in user",
    security=security
)
@jwt_required()
def get_applications(query: ApplicationQuery):

    try:
        current_user_id = int(get_jwt_identity())

        # Pagination parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({
                "error": "Invalid pagination parameters",
                "details": {
                    "page": "Must be at least 1",
                    "per_page": "Must be between 1 and 100"
                },
                "status_code": 400
            }), 400

        # Base query: only current user's applications
        query = JobApplication.query.filter_by(
            user_id=current_user_id
        )

        # Optional status filter
        status_filter = request.args.get("status")

        if status_filter:
            try:
                status_enum = ApplicationStatus(status_filter.upper())
            except ValueError:
                return jsonify({
                    "error": "Invalid application status",
                    "valid_statuses": [
                        status.value for status in ApplicationStatus
                    ],
                    "status_code": 400
                }), 400

            query = query.filter(
                JobApplication.status == status_enum
            )

        # Apply pagination
        pagination = query.order_by(
            JobApplication.id
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        response = jsonify({
            "applications": [
                application.to_dict()
                for application in pagination.items
            ],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        })

        # Pagination headers
        response.headers["X-Total-Count"] = str(pagination.total)
        response.headers["X-Page"] = str(pagination.page)
        response.headers["X-Per-Page"] = str(pagination.per_page)
        response.headers["X-Total-Pages"] = str(pagination.pages)

        return response, 200

    except Exception:
        logger.exception("Error retrieving applications")

        return jsonify({
            "error": "Internal server error",
            "details": {},
            "status_code": 500
        }), 500

# --------------------------------------------------
# CSV Import API
# --------------------------------------------------

@app.route("/applications/import", methods=["POST"])
@jwt_required()
def import_applications():

    current_user_id = int(get_jwt_identity())

    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return jsonify({
            "error": "Please upload a CSV file using the 'file' field"
        }), 400

    if not uploaded_file.filename.lower().endswith(".csv"):
        return jsonify({
            "error": "Only CSV files are allowed"
        }), 400

    try:
        csv_content = uploaded_file.read().decode("utf-8-sig")
        csv_file = io.StringIO(csv_content)

        reader = csv.DictReader(csv_file)

        required_headers = {
            "id",
            "company",
            "role",
            "status",
            "applied_date",
            "notes"
        }

        actual_headers = set(reader.fieldnames or [])
        missing_headers = required_headers - actual_headers

        if missing_headers:
            return jsonify({
                "error": "Invalid CSV headers",
                "missing_headers": sorted(missing_headers)
            }), 400

        created_count = 0
        updated_count = 0
        errors = []

        for row_number, row in enumerate(reader, start=2):

            try:
                with db.session.begin_nested():

                    application_id = (row.get("id") or "").strip()

                    if application_id:
                        if not application_id.isdigit():
                            raise ValueError("Invalid application ID")

                        application = JobApplication.query.filter_by(
                            id=int(application_id),
                            user_id=current_user_id
                        ).first()

                        if not application:
                            raise ValueError(
                                "Application not found or access denied"
                            )

                    else:
                        application = None

                    data = {
                        "company": (row.get("company") or "").strip(),
                        "role": (row.get("role") or "").strip(),
                        "status": (
                            (row.get("status") or "APPLIED").strip().upper()
                        ),
                        "applied_date": (
                            row.get("applied_date") or ""
                        ).strip() or date.today().isoformat(),
                        "notes": (row.get("notes") or "").strip() or None
                    }

                    if not data["role"]:
                        raise ValueError("Role cannot be empty")

                    parsed = ApplicationSchema().load(data)

                    
                    if application:
                        application.company = parsed["company"]
                        application.role = parsed["role"]

                        # Track status changes
                        new_status = ApplicationStatus(
                            parsed["status"]
                        )
                        old_status = application.status

                        if new_status != old_status:
                            current_history = (
                                ApplicationStatusHistory.query
                                .filter_by(
                                    application_id=application.id,
                                    exited_at=None
                                )
                                .order_by(
                                    ApplicationStatusHistory.entered_at.desc()
                                )
                                .first()
                            )

                            if current_history:
                                current_history.exited_at = datetime.utcnow()

                            new_history = ApplicationStatusHistory(
                                application_id=application.id,
                                status=new_status,
                                entered_at=datetime.utcnow(),
                                exited_at=None
                            )

                            db.session.add(new_history)

                        application.status = new_status
                        application.applied_date = parsed["applied_date"]
                        application.notes = parsed["notes"]

                        updated_count += 1

                    else:
                        application = JobApplication(
                            company=parsed["company"],
                            role=parsed["role"],
                            status=ApplicationStatus(parsed["status"]),
                            applied_date=parsed["applied_date"],
                            notes=parsed["notes"],
                            user_id=current_user_id
                        )

                        db.session.add(application)
                        db.session.flush()

                        # Create initial status history
                        new_history = ApplicationStatusHistory(
                            application_id=application.id,
                            status=application.status,
                            entered_at=datetime.utcnow(),
                            exited_at=None
                        )

                        db.session.add(new_history)

                        created_count += 1


            except Exception as row_error:
                errors.append({
                    "row": row_number,
                    "id": row.get("id", ""),
                    "company": row.get("company", ""),
                    "error": str(row_error)
                })

        db.session.commit()

        if errors:
            error_output = io.StringIO()
            error_writer = csv.writer(error_output)

            error_writer.writerow([
                "row",
                "id",
                "company",
                "error"
            ])

            for error in errors:
                error_writer.writerow([
                    error["row"],
                    error["id"],
                    error["company"],
                    error["error"]
                ])

            return Response(
                error_output.getvalue(),
                mimetype="text/csv",
                headers={
                    "Content-Disposition":
                        "attachment; filename=import_error_log.csv",
                    "X-Created-Count": str(created_count),
                    "X-Updated-Count": str(updated_count),
                    "X-Failed-Count": str(len(errors))
                }
            )

        return jsonify({
            "message": "CSV import completed successfully",
            "created": created_count,
            "updated": updated_count,
            "failed": 0
        }), 200

    except Exception:
        db.session.rollback()
        logger.exception("CSV import failed")

        return jsonify({
            "error": "CSV import failed",
            "status_code": 500
        }), 500

# --------------------------------------------------
# Bulk Status Update API
# --------------------------------------------------

@app.route("/applications/bulk-status-update", methods=["POST"])
@jwt_required()
def bulk_status_update():

    current_user_id = int(get_jwt_identity())

    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return jsonify({
            "error": "Please upload a CSV file using the 'file' field"
        }), 400

    if not uploaded_file.filename.lower().endswith(".csv"):
        return jsonify({
            "error": "Only CSV files are allowed"
        }), 400

    try:
        csv_content = uploaded_file.read().decode("utf-8-sig")
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)

        required_headers = {"id", "status"}
        actual_headers = set(reader.fieldnames or [])
        missing_headers = required_headers - actual_headers

        if missing_headers:
            return jsonify({
                "error": "Invalid CSV headers",
                "missing_headers": sorted(missing_headers)
            }), 400

        updated_count = 0
        failed_count = 0
        errors = []

        valid_statuses = {
            status.value for status in ApplicationStatus
        }

        for row_number, row in enumerate(reader, start=2):

            try:
                with db.session.begin_nested():

                    application_id = (
                        row.get("id") or ""
                    ).strip()

                    status_value = (
                        row.get("status") or ""
                    ).strip().upper()

                    if not application_id.isdigit():
                        raise ValueError("Invalid application ID")

                    if status_value not in valid_statuses:
                        raise ValueError(
                            f"Invalid status. Allowed values: "
                            f"{', '.join(sorted(valid_statuses))}"
                        )

                    application = JobApplication.query.filter_by(
                        id=int(application_id),
                        user_id=current_user_id
                    ).first()

                    if not application:
                        raise ValueError(
                            "Application not found or access denied"
                        )

                    
                    new_status = ApplicationStatus(status_value)
                    old_status = application.status

                    if new_status != old_status:

                        # Close the previous status history
                        current_history = (
                            ApplicationStatusHistory.query
                            .filter_by(
                                application_id=application.id,
                                exited_at=None
                            )
                            .order_by(
                                ApplicationStatusHistory.entered_at.desc()
                            )
                            .first()
                        )

                        if current_history:
                            current_history.exited_at = datetime.utcnow()

                        # Create history for the new status
                        new_history = ApplicationStatusHistory(
                            application_id=application.id,
                            status=new_status,
                            entered_at=datetime.utcnow(),
                            exited_at=None
                        )

                        db.session.add(new_history)

                        application.status = new_status

                    db.session.flush()


                updated_count += 1

            except Exception as row_error:

                failed_count += 1

                errors.append({
                    "row": row_number,
                    "id": row.get("id", ""),
                    "status": row.get("status", ""),
                    "error": str(row_error)
                })

        db.session.commit()

        if errors:
            error_output = io.StringIO()
            error_writer = csv.writer(error_output)

            error_writer.writerow([
                "row",
                "id",
                "status",
                "error"
            ])

            for error in errors:
                error_writer.writerow([
                    error["row"],
                    error["id"],
                    error["status"],
                    error["error"]
                ])

            return Response(
                error_output.getvalue(),
                mimetype="text/csv",
                headers={
                    "Content-Disposition":
                        "attachment; filename=bulk_status_error_log.csv",
                    "X-Updated-Count": str(updated_count),
                    "X-Failed-Count": str(failed_count)
                }
            )

        return jsonify({
            "message": "Bulk status update completed successfully",
            "updated": updated_count,
            "failed": 0
        }), 200

    except Exception:
        db.session.rollback()
        logger.exception("Bulk status update failed")

        return jsonify({
            "error": "Bulk status update failed",
            "status_code": 500
        }), 500

# --------------------------------------------------
# Create Application API
# --------------------------------------------------

@app.post(
    "/applications",
    summary="Create application",
    description="Create a new job application for the logged-in user",
    security=security
)
@jwt_required()
def create_application(body: ApplicationCreate):

    data = request.get_json(silent=True)

    try:
        parsed = ApplicationSchema().load(data or {})

        current_user_id = int(get_jwt_identity())

        application = application_service.create_application(
              company=parsed["company"],
              role=parsed["role"],
              status=parsed.get("status", "APPLIED"),
              notes=parsed.get("notes"),
              applied_date=parsed.get("applied_date"),
              user_id=current_user_id
         )

        return jsonify({
            "message": "Application created successfully",
            "application": application.to_dict()
        }), 201

    except ValidationError as error:
        return jsonify({
            "error": "Validation failed",
            "details": error.messages,
            "status_code": 400
        }), 400

    except DuplicateApplication as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 409
        }), 409

    except Exception:
        logger.exception("Error creating application")

        return jsonify({
            "error": "Internal server error",
            "details": {},
            "status_code": 500
        }), 500



# NEW STATS API
@app.get(
    "/applications/stats",
    summary="Get application statistics",
    description="Get application counts grouped by status for the logged-in user",
    security=security
)
@jwt_required()
def application_stats():
    try:
        current_user_id = int(get_jwt_identity())

        counts = {
            status.value: JobApplication.query.filter_by(
                user_id=current_user_id,
                status=status
            ).count()
            for status in ApplicationStatus
        }

        return jsonify({
            "total_applications": sum(counts.values()),
            "status_counts": counts
        }), 200

    except Exception:
        logger.exception("Error retrieving application stats")
        return jsonify({
            "error": "Internal server error",
            "details": {},
            "status_code": 500
        }), 500

# --------------------------------------------------
# Analytics API
# --------------------------------------------------

@app.get(
    "/api/analytics",
    summary="Get application analytics",
    description="Get detailed job application analytics for the logged-in user",
    security=security
)
@jwt_required()
def application_analytics():

    try:
        current_user_id = int(get_jwt_identity())

        # 1. Get all applications of the logged-in user
        applications = JobApplication.query.filter_by(
            user_id=current_user_id
        ).all()

        total_applications = len(applications)

        # 2. Calculate response rate
        interview_count = sum(
            1 for application in applications
            if application.status == ApplicationStatus.INTERVIEW
        )

        response_rate = (
            (interview_count / total_applications) * 100
            if total_applications > 0 else 0
        )

        # 3. Calculate status distribution
        status_distribution = {
            status.value: sum(
                1 for application in applications
                if application.status == status
            )
            for status in ApplicationStatus
        }

        # 4. Calculate average time spent in each status
        history_records = (
            ApplicationStatusHistory.query
            .join(
                JobApplication,
                ApplicationStatusHistory.application_id == JobApplication.id
            )
            .filter(JobApplication.user_id == current_user_id)
            .all()
        )

        current_time = datetime.utcnow()
        status_durations = {
            status.value: [] for status in ApplicationStatus
        }

        for history in history_records:
            end_time = history.exited_at or current_time

            duration_days = (
                end_time - history.entered_at
            ).total_seconds() / 86400

            status_durations[history.status.value].append(
                max(duration_days, 0)
            )

        average_days_per_status = {
            status: round(sum(durations) / len(durations), 2)
            if durations else 0
            for status, durations in status_durations.items()
        }

        # 5. Find the best day of the week to apply
        weekday_counts = {
            day: 0
            for day in [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ]
        }

        for application in applications:
            day = application.applied_date.strftime("%A")
            weekday_counts[day] += 1

        best_day_to_apply = (
            max(weekday_counts, key=weekday_counts.get)
            if total_applications > 0 else None
        )

        return jsonify({
            "total_applications": total_applications,
            "response_rate": round(response_rate, 2),
            "average_days_per_status": average_days_per_status,
            "best_day_to_apply": best_day_to_apply,
            "weekday_application_counts": weekday_counts,
            "status_distribution": status_distribution
        }), 200

    except Exception:
        logger.exception("Error retrieving application analytics")

        return jsonify({
            "error": "Internal server error",
            "status_code": 500
        }), 500

# --------------------------------------------------
# CSV Export API
# --------------------------------------------------

@app.get(
    "/applications/export",
    summary="Export applications as CSV",
    description="Download the logged-in user's applications as a CSV file",
    security=security
)
@jwt_required()
def export_applications():

    try:
        current_user_id = int(get_jwt_identity())

        applications = JobApplication.query.filter_by(
            user_id=current_user_id
        ).order_by(JobApplication.id.asc()).all()

        output = io.StringIO()
        writer = csv.writer(output)

        # CSV column headers
        writer.writerow([
            "id",
            "company",
            "role",
            "status",
            "applied_date",
            "notes"
        ])

        # Write application records
        for application in applications:
            writer.writerow([
                application.id,
                application.company,
                application.role,
                application.status.value,
                application.applied_date.isoformat()
                if application.applied_date else "",
                application.notes or ""
            ])

        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                    "attachment; filename=job_applications.csv"
            }
        )

    except Exception:
        logger.exception("CSV export failed")

        return jsonify({
            "error": "Failed to export applications",
            "status_code": 500
        }), 500



# --------------------------------------------------
# Get Application By ID API
# --------------------------------------------------
@app.get(
    "/applications/<int:application_id>",
    summary="Get application by ID",
    description="Get a specific job application belonging to the logged-in user",
    security=security
)
@jwt_required()
def get_application(path: ApplicationPath):
    application_id = path.application_id

    try:
        current_user_id = int(get_jwt_identity())

        application = JobApplication.query.filter_by(
            id=application_id,
            user_id=current_user_id
        ).first()

        if application is None:
            return jsonify({
                "error": "Application not found",
                "details": {},
                "status_code": 404
            }), 404

        return jsonify(application.to_dict()), 200

    except Exception:
        logger.exception("Error retrieving application")

        return jsonify({
            "error": "Internal server error",
            "details": {},
            "status_code": 500
        }), 500


# --------------------------------------------------
# Update Application API
# --------------------------------------------------
@app.patch(
    "/applications/<int:application_id>",
    summary="Update application",
    description="Partially update a job application belonging to the logged-in user",
    security=security
)
@jwt_required()
def update_application(path: ApplicationPath):
    application_id = path.application_id

    data = request.get_json(silent=True)

    try:
        if not isinstance(data, dict) or not data:
            return jsonify({
                "error": "At least one field is required",
                "details": {},
                "status_code": 400
            }), 400

        # Validate only the fields provided by the user
        parsed = ApplicationSchema().load(
            data,
            partial=True
        )

        # Remove default values for fields not included in PUT request
        for field in ("status", "applied_date", "notes"):
            if field not in data:
                parsed.pop(field, None)

        if not parsed:
            return jsonify({
                "error": "At least one valid field is required",
                "details": {},
                "status_code": 400
            }), 400
        current_user_id = int(get_jwt_identity())

        owned_application = JobApplication.query.filter_by(
            id=application_id,
            user_id=current_user_id
        ).first()

        if owned_application is None:
            return jsonify({
                "error": "Application not found",
                "details": {},
                "status_code": 404
            }), 404

        # Prevent changing application ownership
        parsed.pop("user_id", None)

        application = application_service.update_application(
            application_id,
            parsed
        )

        return jsonify({
            "message": "Application updated successfully",
            "application": application.to_dict()
        }), 200

    except ValidationError as error:
        return jsonify({
            "error": "Validation failed",
            "details": error.messages,
            "status_code": 400
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 400
        }), 400

    except ApplicationNotFound as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 404
        }), 404

    except DuplicateApplication as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 409
        }), 409

    except Exception:
        logger.exception("Error updating application")

        return jsonify({
            "error": "Internal server error",
            "details": {},
            "status_code": 500
        }), 500


# --------------------------------------------------
# Delete Application API
# --------------------------------------------------
@app.delete(
    "/applications/<int:application_id>",
    summary="Delete application",
    description="Delete a job application belonging to the logged-in user",
    security=security
)
@jwt_required()
def delete_application(path: ApplicationPath):
    application_id = path.application_id
    
    try:
        current_user_id = int(get_jwt_identity())

        print("DEBUG DELETE FUNCTION CALLED")
        print("DEBUG application_id:", application_id)
        print("DEBUG current_user_id:", current_user_id)

        # Find application belonging to current user
        application_by_id = JobApplication.query.filter_by(
              id=application_id
        ).first()

        print("DEBUG application by ID:", application_by_id)

        if application_by_id:
           print("DEBUG DB application ID:", application_by_id.id)
           print("DEBUG DB user ID:", application_by_id.user_id)
           print("DEBUG DB company:", application_by_id.company)

        application = JobApplication.query.filter_by(
            id=application_id,
            user_id=current_user_id
        ).first()

        print("DEBUG ownership query result:", application)

        print("DEBUG application found:", application is not None)

        if application is None:
            return jsonify({
                "error": "Application not found",
                "details": {},
                "status_code": 404
            }), 404

        resume_path = application.resume_path

        # Delete application
        deleted_application = application_service.delete_application(
            application_id
        )

        # Delete associated resume file
        delete_resume_file(resume_path)

        return jsonify({
            "message": "Application deleted successfully",
            "application": deleted_application.to_dict()
        }), 200

    except ApplicationNotFound as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 404
        }), 404

    except Exception:
        db.session.rollback()
        logger.exception("Error deleting application")

        return jsonify({
            "error": "Internal server error",
            "details": {},
            "status_code": 500
        }), 500

# --------------------------------------------------
# Upload Resume API
# --------------------------------------------------

@app.route(
    "/applications/<int:application_id>/resume",
    methods=["POST"]
)
@jwt_required()
def upload_resume(application_id):

    try:
        current_user_id = int(get_jwt_identity())
        
        application = JobApplication.query.filter_by(
            id=application_id,
            user_id=current_user_id
        ).first()

        if application is None:
            return jsonify({
                "error": "Application not found",
                "details": {},
                "status_code": 404
            }), 404

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

        file.save(file_path)

        old_resume_path = application.resume_path

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
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 404
        }), 404

    except Exception:
        db.session.rollback()
        logger.exception("Error uploading resume")

        return jsonify({
            "error": "Failed to upload resume",
            "details": {},
            "status_code": 500
        }), 500


# --------------------------------------------------
# Serve Uploaded Resume API
# --------------------------------------------------
@app.route("/files/<path:filename>", methods=["GET"])
@jwt_required()
def serve_resume(filename):

    try:
        current_user_id = int(get_jwt_identity())

        application = JobApplication.query.filter_by(
            resume_path=filename,
            user_id=current_user_id
        ).first()

        if application is None:
            return jsonify({
                "error": "Resume file not found",
                "details": {},
                "status_code": 404
            }), 404

        return send_from_directory(
            app.root_path,
            filename,
            as_attachment=False
        )

    except Exception:
        logger.exception("Error serving resume")

        return jsonify({
            "error": "Resume file not found",
            "details": {},
            "status_code": 404
        }), 404

# --------------------------------------------------
# Extract Resume Skills API
# --------------------------------------------------

@app.route(
    "/applications/<int:application_id>/resume/skills",
    methods=["GET"]
)
@jwt_required()
def get_resume_skills(application_id):

    try:
        current_user_id = int(get_jwt_identity())

        application = JobApplication.query.filter_by(
            id=application_id,
            user_id=current_user_id
        ).first()

        if application is None:
            return jsonify({
                "error": "Application not found",
                "details": {},
                "status_code": 404
            }), 404

        if not application.resume_path:
            return jsonify({
                "error": "No resume uploaded for this application",
                "details": {},
                "status_code": 404
            }), 404

        filename = os.path.basename(application.resume_path)

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        if not os.path.isfile(file_path):
            return jsonify({
                "error": "Resume file not found",
                "details": {},
                "status_code": 404
            }), 404

        extracted_text = extract_pdf_text(file_path)

        skills = extract_skills(extracted_text)

        return jsonify({
            "application_id": application_id,
            "extracted_text": extracted_text,
            "skills": skills
        }), 200

    except ApplicationNotFound as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 404
        }), 404

    except ValueError as error:
        return jsonify({
            "error": str(error),
            "details": {},
            "status_code": 400
        }), 400

    except Exception:
        logger.exception("Error extracting resume skills")

        return jsonify({
            "error": "Failed to extract resume text",
            "details": {},
            "status_code": 500
        }), 500


# --------------------------------------------------
# Global Error Handlers
# --------------------------------------------------

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad request",
        "details": {},
        "status_code": 400
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource not found",
        "details": {},
        "status_code": 404
    }), 404


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "File size exceeds the 5 MB limit",
        "details": {},
        "status_code": 413
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    logger.error("Internal server error: %s", error)

    return jsonify({
        "error": "Internal server error",
        "details": {},
        "status_code": 500
    }), 500


# Job Search Query Schema
class JobSearchQuery(BaseModel):
    q: str = Field(..., min_length=1, description="Job keyword")
    location: str = Field(..., min_length=1, description="Job location")


# External Job Search API
@app.get("/api/jobs/search")
def search_external_jobs(query: JobSearchQuery):

    keyword = query.q.strip()
    location = query.location.strip()

    cache_key = f"jobs:{keyword.lower()}:{location.lower()}"

    # Check Redis cache
    cached_jobs = cache.get(cache_key)

    if cached_jobs is not None:
        logger.info("Job search cache HIT: %s", cache_key)
        return jsonify({
            "source": "cache",
            "count": len(cached_jobs),
            "results": cached_jobs
        }), 200

    logger.info("Job search cache MISS: %s", cache_key)

    try:
        jobs = job_search_service.search_jobs(
            keyword=keyword,
            location=location,
            results_per_page=5
        )

        # Validate results using JobSuggestion DTO
        validated_jobs = [
            JobSuggestion(**job).model_dump()
            for job in jobs
        ]

        # Store results in Redis for 30 minutes
        cache.set(cache_key, validated_jobs, timeout=1800)

        return jsonify({
            "source": "adzuna_api",
            "count": len(validated_jobs),
            "results": validated_jobs
        }), 200

    except RuntimeError:
        logger.exception("Job search configuration error")
        return jsonify({"error": "Job search API is not configured"}), 503

    except Exception:
        logger.exception("External job search failed")
        return jsonify({"error": "Unable to search jobs at the moment"}), 502

# --------------------------------------------------
# Run Flask Application
# --------------------------------------------------

if __name__ == "__main__":

    from services.scheduler_service import start_scheduler

    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler(app)

    app.run(debug=True)