# Job Application Tracker SaaS

A Flask-based Job Application Tracker SaaS that helps users manage job applications, track application statuses, upload resumes, and extract skills from PDF resumes.

The application includes secure JWT-based authentication, RESTful APIs, database migrations, automated testing, API documentation, and continuous integration using GitHub Actions.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **ORM:** Flask-SQLAlchemy
- **Migrations:** Flask-Migrate, Alembic
- **Validation:** Marshmallow, Pydantic
- **API Documentation:** Flask-OpenAPI3, Swagger UI
- **PDF Processing:** PyPDF2
- **Authentication:** JWT (JSON Web Tokens)
- **Testing:** Pytest, Factory Boy, Pytest-Cov
- **CI/CD:** GitHub Actions
- **Version Control:** Git & GitHub
- **API Testing:** Postman
- **Containerization:** Docker

---

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
- Successfully pushed Day 7 changes to GitHub.

### Day 8 – REST API Enhancement, Pagination & Swagger Documentation

- Implemented and enhanced REST API endpoints using Flask-OpenAPI3.
- Added complete Job Application CRUD operations:
  - `GET /applications` – Retrieve applications.
  - `POST /applications` – Create a new application.
  - `GET /applications/{application_id}` – Retrieve an application by ID.
  - `PATCH /applications/{application_id}` – Update an application.
  - `DELETE /applications/{application_id}` – Delete an application.
- Implemented pagination for application listing.
- Added filtering applications by status.
- Implemented application statistics API:
  - `GET /applications/stats`
- Added Pydantic-based request and path validation.
- Integrated Swagger UI for interactive API documentation.
- Tested all six API endpoints using Postman.
- Exported Postman collection to `postman/Job-Application-Tracker.postman_collection.json`.
- Updated API test cases to support Flask-OpenAPI3 validation.
- Successfully executed the complete Pytest suite.
- Achieved **92 passed tests**.
- Committed Day 8 changes to Git.
- Successfully synchronized local and remote Git branches using Git rebase.
- Successfully pushed Day 8 changes to GitHub.

---

## Project Structure

```text
Job-Application-Tracker/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── api/
│
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
├── postman/
│   └── Job-Application-Tracker.postman_collection.json
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

## API Documentation

The project uses Swagger UI to provide interactive API documentation.

**Swagger URL:**

```text
http://127.0.0.1:5000/openapi/swagger
```

You can explore and test the available API endpoints directly through Swagger UI.

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

**Application URL:**

```text
http://127.0.0.1:5000
```

**Swagger Documentation:**

```text
http://127.0.0.1:5000/openapi/swagger
```

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
| Day 6 Tests Passed | 83 |
| Day 6 Overall Coverage | 84% |
| Day 6 GitHub Actions CI | Passed |
| Day 7 JWT Authentication | Implemented |
| Day 8 REST API Endpoints | 6 |
| Day 8 Pytest Results | **92 Passed** |
| Day 8 Swagger Documentation | Completed |
| Day 8 Postman Testing | Completed |

*Day 6 coverage metrics are historical results. Day 8 test count reflects the latest successful Pytest execution.*

## GitHub Repository

[Job Application Tracker – GitHub](https://github.com/Prasanna-20740/Job-Application-Tracker)

## Current Project Status

**Completed:** Day 1 – Day 8

**Latest Development:**
- JWT Authentication and Token Blocklist
- RESTful CRUD API Development
- Pagination and Status Filtering
- Application Statistics API
- Swagger API Documentation
- Postman API Testing
- Automated Testing with Pytest
- GitHub Actions CI Integration

**Latest Test Result:** 92 Passed

**Repository Status:** Day 8 changes successfully committed and pushed to GitHub.

---

Developed as a internship project.
