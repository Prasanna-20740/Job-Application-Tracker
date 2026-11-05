from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres123@localhost:5434/job_tracker"
)

db = SQLAlchemy(app)

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

@app.route("/")
def home():
    return {
        "message": "Job Application Tracker API is running!",
        "endpoints": {
            "applications": "/applications"
        }
    }

@app.route("/applications", methods=["GET"])
def get_applications():
    apps = JobApplication.query.all()
    return jsonify([job.to_dict() for job in apps])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
