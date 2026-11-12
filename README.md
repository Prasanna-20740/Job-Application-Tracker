# Job Application Tracker SaaS

A Flask-based Job Application Tracker SaaS that helps users manage job applications, track application statuses, upload resumes, and extract skills from PDF resumes. The application also provides secure JWT-based authentication and automated testing.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **ORM:** Flask-SQLAlchemy
- **Migrations:** Flask-Migrate, Alembic
- **Validation:** Marshmallow
- **PDF Processing:** PyPDF2
- **Authentication:** JWT (JSON Web Tokens)
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

### Day 7 – JWT Authentication & Advanced Testing

- Implemented JWT-based authentication.
- Created a dedicated `auth/` package for authentication routes.
- Implemented user authentication and token generation.
- Added JWT token validation.
- Implemented token blocklist functionality for invalidating revoked tokens.
- Integrated authentication functionality with the Flask application.
- Created a new Alembic database migration for JWT authentication and token blocklist support.
- Added authentication test cases in `tests/test_auth.py`.
- Expanded application API test coverage.
- Improved file upload test cases.
- Updated reusable test fixtures in `tests/conftest.py`.
- Updated application dependencies in `requirements.txt`.
- Validated Python code using `py_compile`.
- Executed automated tests using Pytest.
- Committed all Day 7 changes to Git.
- Successfully synchronized local changes with the remote GitHub repository using Git rebase.
- Successfully pushed Day 7 changes to GitHub.

## Project Structure

```text
Job-Application-Tracker/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── api/
├── auth/
│   ├── __init__.py
│   └── routes.py
│
├── migrations/
│   └── versions/
│
├── models/
├── schemas/
├── services/
│
├── tests/
│   ├── conftest.py
│   ├── factories.py
│   ├── test_auth.py
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
| Total Tests Passed (Day 6) | 83 |
| Overall Coverage (Day 6) | 84% |
| app.py Coverage (Day 6) | 85% |
| Application Service Coverage (Day 6) | 82% |
| GitHub Actions CI | Passed |
| Day 7 Authentication Tests | Implemented |

*Day 6 metrics are retained as historical results. Day 7 updated test results should be added after generating a fresh coverage report.*

## GitHub Repository

[Job Application Tracker – GitHub](https://github.com/Prasanna-20740/Job-Application-Tracker)

## Current Status

**Completed:** Day 1 – Day 7

**Latest Development:** JWT Authentication, Token Blocklist, and Expanded Automated Testing.

**Repository Status:** Day 7 changes successfully pushed to GitHub.

---

Developed as a hands-on Python Flask SaaS internship project.
