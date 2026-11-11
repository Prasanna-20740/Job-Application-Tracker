# Job Application Tracker SaaS

A Flask-based Job Application Tracker SaaS that helps users manage job applications, track application statuses, upload resumes, and extract skills from PDF resumes.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **ORM:** Flask-SQLAlchemy
- **Migrations:** Flask-Migrate, Alembic
- **Validation:** Marshmallow
- **PDF Processing:** PyPDF2
- **Testing:** Pytest, Factory Boy, Pytest-Cov
- **CI/CD:** GitHub Actions
- **Version Control:** Git & GitHub

## Project Progress

### Day 1 – Project Setup & Architecture
- Defined the Job Application Tracker SaaS use case.
- Created Python virtual environment.
- Installed Flask and Flask-SQLAlchemy.
- Configured PostgreSQL using Docker.
- Established project folder structure:
  - `api/`
  - `models/`
  - `services/`
  - `tests/`

### Day 2 – Database & Models
- Created JobApplication model.
- Added application fields:
  - Company
  - Role
  - Status
  - Applied Date
  - Notes
- Created ApplicationStatus enum:
  - APPLIED
  - PHONE_SCREEN
  - INTERVIEW
  - OFFER
  - REJECTED
- Created User model for multi-user support.
- Configured Alembic database migrations.
- Created initial database migration.

### Day 3 – REST API Development
- Implemented Flask REST API endpoints.
- Added application CRUD operations:
  - Create application
  - Get applications
  - Get application by ID
  - Update application
  - Delete application
- Added request validation.
- Implemented structured error handling.
- Added user management endpoints.

### Day 4 – Resume Upload & PDF Processing
- Implemented PDF resume upload functionality.
- Added file type and PDF signature validation.
- Configured upload size restrictions.
- Implemented resume storage.
- Extracted text from PDF resumes using PyPDF2.
- Added skill extraction functionality.
- Created resume skills API endpoint.

### Day 5 – Service Layer & Application Logic
- Implemented ApplicationService.
- Separated business logic from API routes.
- Added application creation, retrieval, update, deletion, and listing operations.
- Implemented duplicate application handling.
- Added custom exceptions:
  - ApplicationNotFound
  - DuplicateApplication
- Improved code organization and maintainability.

### Day 6 – Pytest Testing & GitHub Actions CI
- Configured Pytest testing framework.
- Created reusable test fixtures using `conftest.py`.
- Integrated Factory Boy for test data generation.
- Added test coverage for:
  - Application Service
  - Application API
  - File Upload
  - Helper Functions
- Configured SQLite database for isolated tests.
- Added Pytest coverage reporting.
- Achieved **84% overall test coverage**.
- Successfully passed **83 tests**.
- Configured GitHub Actions CI workflow.
- Automated test execution on push and pull requests.
- Added `.gitignore` and `.coveragerc`.
- Successfully verified GitHub Actions CI with a green check.

## Project Structure

```text
Job-Application-Tracker/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── migrations/
├── models/
├── schemas/
├── services/
├── tests/
│   ├── conftest.py
│   ├── factories.py
│   ├── test_application_api.py
│   ├── test_application_service.py
│   ├── test_file_upload.py
│   └── test_helpers.py
│
├── uploads/
├── app.py
├── seed.py
├── docker-compose.yml
├── requirements.txt
├── .coveragerc
├── .gitignore
└── README.md
```

## Running the Project Locally

### 1. Clone Repository

```bash
git clone https://github.com/Prasanna-20740/Job-Application-Tracker.git
cd Job-Application-Tracker
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start PostgreSQL

```bash
docker compose up -d
```

### 6. Run Database Migrations

```bash
flask db upgrade
```

### 7. Start Flask Application

```bash
python app.py
```

Application URL: `http://127.0.0.1:5000`

## Running Tests

Run all tests:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov=services --cov-report=term-missing
```

## Test Results

| Metric | Result |
|---|---:|
| Total Tests Passed | 83 |
| Overall Coverage | 84% |
| app.py Coverage | 85% |
| Application Service Coverage | 82% |
| GitHub Actions CI | Passed |

## GitHub Repository

[Job Application Tracker – GitHub](https://github.com/Prasanna-20740/Job-Application-Tracker)

## Current Status

**Completed:** Day 1 – Day 6

**Next:** Day 7 – Upcoming Development

---

Developed as a hands-on Python Flask SaaS internship project.
