# Job Application Tracker SaaS

A Flask-based Job Application Tracker SaaS that helps users manage job applications, monitor application progress, upload resumes, extract skills from PDF resumes, discover external job opportunities, and schedule interview reminders.

The application provides secure JWT authentication, RESTful APIs, PostgreSQL integration, Redis caching, automated email notifications, API documentation, and automated testing.

**GitHub Repository:** https://github.com/Prasanna-20740/Job-Application-Tracker

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Development Progress](#project-development-progress)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Email Notification System](#email-notification-system)
- [Automated Testing](#automated-testing)
- [Current Project Status](#current-project-status)

---

## Features

- User registration and login using JWT authentication.
- Secure access and refresh token management.
- Job application CRUD operations.
- Application status tracking.
- Resume upload and PDF text extraction.
- Resume skill extraction.
- Application statistics and pagination.
- External job search using Adzuna API.
- Redis caching for job search results.
- Interactive Swagger API documentation.
- Postman API collection.
- Weekly job application digest emails.
- Automated interview reminder emails.
- HTML email templates using Jinja2.
- Background scheduling using APScheduler.
- Automated testing using Pytest.
- GitHub Actions CI workflow.

---

## Tech Stack

### Backend
- Python
- Flask
- Flask-OpenAPI3

### Database and ORM
- PostgreSQL
- SQLite (Testing)
- Flask-SQLAlchemy
- Flask-Migrate
- Alembic

### Authentication and Security
- JWT (JSON Web Tokens)
- Flask-JWT-Extended
- Token Blocklist
- Protected API Routes

### Validation and Serialization
- Marshmallow
- Pydantic

### External API Integration
- Adzuna Job Search API
- Python Requests

### Caching
- Redis
- Flask-Caching

### Email Notifications
- Flask-Mail
- Mailtrap SMTP
- Jinja2 HTML Templates
- APScheduler

### PDF Processing
- PyPDF2
- PDF Text Extraction
- Resume Skill Extraction

### Testing and DevOps
- Pytest
- Factory Boy
- Pytest-Cov
- GitHub Actions
- Docker
- Docker Compose
- Git and GitHub
- Postman
- VS Code

---

## Project Development Progress

### Day 1 – Project Setup and Architecture

- Planned the Job Application Tracker SaaS.
- Identified application requirements and features.
- Designed the modular Flask backend architecture.
- Created the Python virtual environment.
- Installed Flask and Flask-SQLAlchemy.
- Configured PostgreSQL using Docker.
- Initialized Git and GitHub repository.

### Day 2 – Database Design and Models

- Integrated PostgreSQL with Flask.
- Configured SQLAlchemy ORM.
- Integrated Flask-Migrate and Alembic.
- Created JobApplication model.
- Created User model.
- Implemented application status using Python Enum.
- Designed user and application relationships.

### Day 3 – REST API Development

- Implemented RESTful APIs.
- Developed application CRUD operations.
- Implemented application creation, retrieval, updating, and deletion.
- Added request validation.
- Implemented structured error handling.
- Added user management endpoints.

### Day 4 – Resume Upload and PDF Processing

- Implemented PDF resume upload.
- Added file type and PDF signature validation.
- Configured file storage.
- Integrated PyPDF2.
- Implemented PDF text extraction.
- Developed basic resume skill extraction.
- Created resume-related API endpoints.

### Day 5 – Service Layer and Business Logic

- Created ApplicationService.
- Separated business logic from API routes.
- Implemented reusable service methods.
- Added custom exceptions:
  - ApplicationNotFound
  - DuplicateApplication
- Improved error handling and code organization.

### Day 6 – Pytest and GitHub Actions CI

- Configured Pytest.
- Created reusable test fixtures.
- Integrated Factory Boy.
- Configured SQLite for testing.
- Integrated pytest-cov.
- Created application API and service tests.
- Configured GitHub Actions CI.
- Successfully passed 83 tests.
- Achieved 84% overall test coverage.

### Day 7 – JWT Authentication and Advanced Testing

- Integrated Flask-JWT-Extended.
- Implemented user registration and login.
- Implemented access and refresh tokens.
- Configured token expiration.
- Implemented token blocklist.
- Added logout and token revocation.
- Protected application API routes.
- Created authentication test cases.

### Day 8 – REST API Enhancement and Swagger Documentation

- Integrated Flask-OpenAPI3.
- Configured Swagger UI.
- Documented REST API endpoints.
- Implemented application pagination.
- Added application statistics.
- Added pagination response headers.
- Created Postman collection.
- Tested CRUD operations and API responses.

Swagger UI:

`http://127.0.0.1:5000/openapi/swagger`

### Day 9 – External Job Search API and Redis Caching

**Adzuna API Integration**

- Integrated Adzuna Job Search API.
- Configured API credentials using environment variables.
- Implemented keyword-based job search.
- Implemented location-based job search.
- Created JobSearchService.
- Created Pydantic JobSuggestion DTO.
- Added external API error handling.

**Redis Integration**

- Integrated Redis with Flask.
- Configured Redis using Docker Compose.
- Implemented job search result caching.
- Configured 30-minute cache expiration.
- Implemented cache hit and cache miss detection.

API example:

`GET /api/jobs/search?q=python&location=chennai`

Cache verification:
- First request: `source: adzuna_api`
- Subsequent request: `source: cache`

### Day 10 – Email Notifications and Interview Reminders

**Flask-Mail and SMTP Integration**

- Integrated Flask-Mail.
- Configured Mailtrap Email Sandbox.
- Configured SMTP credentials using environment variables.
- Verified email delivery through Mailtrap.

**Weekly Job Application Digest**

- Retrieves applications updated during the last 7 days.
- Generates a weekly application summary.
- Displays company, role, and application status.
- Sends digest emails to registered users.
- Configured weekly scheduling for Monday at 9:00 AM.

**Interview Scheduling and Reminders**

- Created Interview database model.
- Linked interviews with job applications.
- Added interview date and time.
- Added interview type, meeting link, and notes.
- Implemented automatic interview reminder emails.
- Checks upcoming interviews every 5 minutes.
- Sends reminders approximately 24 hours before interviews.
- Uses `reminder_sent` to prevent duplicate reminders.

**HTML Email Templates**

Created Jinja2 email templates:

- `templates/emails/weekly_digest.html`
- `templates/emails/interview_reminder.html`

**Background Scheduling**

Integrated APScheduler for:
- Weekly digest scheduling.
- Automatic interview reminder checks.

**Testing**

- Weekly digest email successfully delivered to Mailtrap.
- Interview reminder email successfully delivered to Mailtrap.
- Verified dynamic email content and HTML formatting.
- Existing automated test suite passed: 92 tests.

---

## API Endpoints

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | User login |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Revoke authentication token |

### Job Application APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications` | Retrieve applications with pagination |
| POST | `/applications` | Create application |
| GET | `/applications/stats` | Application statistics |
| GET | `/applications/{application_id}` | Retrieve application |
| PATCH | `/applications/{application_id}` | Update application |
| DELETE | `/applications/{application_id}` | Delete application |

### Resume APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/applications/{application_id}/resume` | Upload PDF resume |
| GET | `/applications/{application_id}/skills` | Extract resume skills |
| GET | `/files/{filename}` | Access uploaded file where supported |

### External Job Search API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs/search` | Search external jobs using Adzuna |

Example:

`GET /api/jobs/search?q=python&location=chennai`

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
├── auth/
│   ├── __init__.py
│   └── routes.py
│
├── migrations/
│   └── versions/
│
├── models/
├── schemas/
│   └── job_suggestion.py
│
├── services/
│   ├── job_search_service.py
│   ├── email_service.py
│   └── scheduler_service.py
│
├── templates/
│   └── emails/
│       ├── weekly_digest.html
│       └── interview_reminder.html
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
├── uploads/
│
├── app.py
├── seed.py
├── docker-compose.yml
├── requirements.txt
├── .coveragerc
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Prerequisites

- Python 3.10+
- PostgreSQL
- Docker Desktop
- Redis
- Git

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

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Refer to the Environment Configuration section below.

### 6. Start PostgreSQL and Redis

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

Verify Redis:

```bash
docker exec job_tracker_redis redis-cli ping
```

Expected output:

```text
PONG
```

### 7. Run Database Migrations

```bash
flask --app app db upgrade
```

### 8. Start Flask Application

```bash
python app.py
```

Application URL:

`http://127.0.0.1:5000`

Swagger UI:

`http://127.0.0.1:5000/openapi/swagger`

Keep the application process running for the background scheduler jobs to execute.

---

## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
# Adzuna API
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

# Redis
REDIS_URL=redis://localhost:6379/0

# Mailtrap SMTP
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=testing@example.com
```

Configure the PostgreSQL connection according to the database settings used by the application.

**Security:** Never commit `.env` or real API credentials to GitHub. Use placeholder values in `.env.example`.

---

## Email Notification System

### Weekly Digest

- Runs every Monday at 9:00 AM.
- Retrieves applications updated during the previous 7 days.
- Sends an HTML summary email.
- Displays application details.

### Interview Reminder

- Scheduler checks every 5 minutes.
- Finds interviews approximately 24 hours before their scheduled time.
- Sends an HTML reminder email.
- Updates the `reminder_sent` database field after successful delivery.

### Email Testing

Mailtrap Email Sandbox was used to verify:
- SMTP connectivity.
- Weekly digest delivery.
- Interview reminder delivery.
- Jinja2 dynamic content.
- HTML email rendering.

---

## Automated Testing

Run all tests:

```bash
pytest -q
```

Run tests with coverage:

```bash
pytest --cov=app --cov=services --cov-report=term-missing
```

Run authentication tests:

```bash
pytest tests/test_auth.py -v
```

### Latest Test Results – Day 10

| Metric | Result |
|---|---:|
| Total Tests Passed | 92 |
| Tests Failed | 0 |
| Execution Time | 1.74 seconds |
| Weekly Digest Email | Verified |
| Interview Reminder Email | Verified |
| HTML Templates | Verified |

Historical Day 6 coverage:
- Overall coverage: 84%
- app.py coverage: 85%
- Application Service coverage: 82%

## Day 11 – CSV Import, Export and Bulk Updates

### Features Implemented

**1. CSV Export**
- Export all applications belonging to the authenticated user.
- Download application records as `job_applications.csv`.
- Includes ID, company, role, status, applied date and notes.
- Protects user data through JWT authentication and user-level filtering.

**2. CSV Import**
- Upload application records using a CSV file.
- Validate required CSV headers and application fields.
- Create new applications when ID is empty.
- Update existing applications using their application ID.
- Skip invalid rows without stopping the entire import.
- Generate `import_error_log.csv` for failed rows.

**3. Bulk Status Update**
- Update multiple application statuses using a CSV file.
- Validate application IDs and status values.
- Support statuses: APPLIED, PHONE_SCREEN, INTERVIEW, OFFER and REJECTED.
- Skip invalid records and generate an error log.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications/export` | Export applications as CSV |
| POST | `/applications/import` | Import and update applications using CSV |
| POST | `/applications/bulk-status-update` | Update multiple application statuses |

All three endpoints require JWT authentication.

### CSV Round-Trip Testing

- Exported application records to CSV.
- Edited three application records.
- Re-imported the modified CSV.
- Verified updated roles and statuses through the applications API.
- Confirmed that existing records were updated without creating duplicates.
- Tested invalid rows and error log generation.

### Automated Testing

Added `tests/test_csv_api.py` with 8 automated tests covering:
- CSV export and user data isolation.
- CSV import create and update operations.
- Invalid row handling and error logs.
- Missing header validation.
- Bulk status update success and failure cases.

**Test Results:**
- Total tests: 100 passed
- Failed tests: 0
- Application code coverage: 81%

### Day 11 Deliverable

Completed CSV export/import round-trip, validation, error reporting and bulk status updates with successful manual and automated testing.


---

## Current Project Status

**Completed Development: Day 1 – Day 10**

### Major Features Completed

- Flask backend architecture.
- PostgreSQL database integration.
- SQLAlchemy models and Alembic migrations.
- RESTful CRUD APIs.
- Multi-user database structure.
- PDF resume upload and skill extraction.
- Service-layer architecture.
- JWT authentication and token management.
- Swagger API documentation.
- Application pagination and statistics.
- Postman API collection.
- Adzuna external job search.
- Pydantic DTO validation.
- Redis caching.
- Docker-based PostgreSQL and Redis services.
- Pytest automated testing.
- GitHub Actions CI.
- Flask-Mail SMTP integration.
- Weekly application digest emails.
- Interview scheduling model.
- Automated interview reminders.
- Jinja2 HTML email templates.
- APScheduler background jobs.

### Latest Test Execution

**92 Passed | 0 Failed**

---

## Developer

**Prasanna P**

GitHub: https://github.com/Prasanna-20740

LinkedIn: https://www.linkedin.com/in/prasanna-p20/

Portfolio: https://prasanna-p.vercel.app/

---

Developed as a hands-on Python Flask SaaS project, focusing on backend development, REST API design, database management, authentication, external API integration, caching, email automation, automated testing, and CI/CD.
