
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres123@localhost:5434/job_tracker"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Job Application Model
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="APPLIED")

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "status": self.status
        }


# Home API
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Job Application Tracker API is running!",
        "endpoints": {
            "get_all_applications": "/applications",
            "create_application": "/applications",
            "get_application_by_id": "/applications/<id>",
            "update_application": "/applications/<id>"
        }
    }), 200


# Day 1 - Get All Applications API
@app.route("/applications", methods=["GET"])
def get_applications():
    apps = JobApplication.query.all()

    return jsonify([
        job.to_dict() for job in apps
    ]), 200


# Day 2 - Create New Application API
@app.route("/applications", methods=["POST"])
def add_application():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Valid JSON data is required"
        }), 400

    company = data.get("company")
    role = data.get("role")
    status = data.get("status", "APPLIED")

    # Validate company
    if not isinstance(company, str) or not company.strip():
        return jsonify({
            "error": "Company name is required"
        }), 400

    # Validate role
    if not isinstance(role, str) or not role.strip():
        return jsonify({
            "error": "Job role is required"
        }), 400

    # Validate status
    if not isinstance(status, str) or not status.strip():
        return jsonify({
            "error": "Valid application status is required"
        }), 400

    new_application = JobApplication(
        company=company.strip(),
        role=role.strip(),
        status=status.strip().upper()
    )

    try:
        db.session.add(new_application)
        db.session.commit()

        return jsonify({
            "message": "Application added successfully",
            "application": new_application.to_dict()
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to add application"
        }), 500


# Day 3 - Get Application by ID API
@app.route("/applications/<int:application_id>", methods=["GET"])
def get_application_by_id(application_id):

    application = db.session.get(
        JobApplication,
        application_id
    )

    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    return jsonify(application.to_dict()), 200


# Day 4 - Update Application API
@app.route("/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):

    # Find application by ID
    application = db.session.get(
        JobApplication,
        application_id
    )

    # Check application exists
    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    # Get JSON data
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Valid JSON data is required"
        }), 400

    # Validate and update company
    if "company" in data:
        company = data["company"]

        if not isinstance(company, str) or not company.strip():
            return jsonify({
                "error": "Valid company name is required"
            }), 400

        application.company = company.strip()

    # Validate and update role
    if "role" in data:
        role = data["role"]

        if not isinstance(role, str) or not role.strip():
            return jsonify({
                "error": "Valid job role is required"
            }), 400

        application.role = role.strip()

    # Validate and update status
    if "status" in data:
        status = data["status"]

        if not isinstance(status, str) or not status.strip():
            return jsonify({
                "error": "Valid application status is required"
            }), 400

        application.status = status.strip().upper()

    try:
        db.session.commit()

        return jsonify({
            "message": "Application updated successfully",
            "application": application.to_dict()
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to update application"
        }), 500


# Create Database Tables
with app.app_context():
    db.create_all()


# Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
