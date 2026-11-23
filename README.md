# Job Application Tracker SaaS

A Flask-based Job Application Tracker SaaS that helps users manage job applications, monitor application progress, upload resumes, extract skills from PDF resumes, discover external job opportunities, analyze application performance, and schedule interview reminders.

The application provides secure JWT authentication, RESTful APIs, PostgreSQL integration, Redis caching, automated email notifications, analytics, API documentation, and automated testing.

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
- Application status tracking and history.
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
- CSV application import and export.
- Bulk application status updates.
- Application analytics and performance tracking.
- Response rate calculation.
- Average time spent in each application status.
- Best weekday to apply analysis.
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

### Data Import and Export
- Python CSV
- CSV Import and Export
- Bulk Status Updates

### Analytics
- SQLAlchemy Queries
- Application Status History
- Response Rate Calculation
- Time-in-Stage Analysis
- Weekday Application Analysis

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

### Day 1 â€“ Project Setup and Architecture

- Planned the Job Application Tracker SaaS.
- Identified application requirements and features.
- Designed the modular Flask backend architecture.
- Created the Python virtual environment.
- Installed Flask and Flask-SQLAlchemy.
- Configured PostgreSQL using Docker.
- Initialized Git and GitHub repository.

### Day 2 â€“ Database Design and Models

- Integrated PostgreSQL with Flask.
- Configured SQLAlchemy ORM.
- Integrated Flask-Migrate and Alembic.
- Created JobApplication model.
- Created User model.
- Implemented application status using Python Enum.
- Designed user and application relationships.

### Day 3 â€“ REST API Development

- Implemented RESTful APIs.
- Developed application CRUD operations.
- Implemented application creation, retrieval, updating, and deletion.
- Added request validation.
- Implemented structured error handling.
- Added user management endpoints.

### Day 4 â€“ Resume Upload and PDF Processing

- Implemented PDF resume upload.
- Added file type and PDF signature validation.
- Configured file storage.
- Integrated PyPDF2.
- Implemented PDF text extraction.
- Developed basic resume skill extraction.
- Created resume-related API endpoints.

### Day 5 â€“ Service Layer and Business Logic

- Created ApplicationService.
- Separated business logic from API routes.
- Implemented reusable service methods.
- Added custom exceptions:
  - ApplicationNotFound
  - DuplicateApplication
- Improved error handling and code organization.

### Day 6 â€“ Pytest and GitHub Actions CI

- Configured Pytest.
- Created reusable test fixtures.
- Integrated Factory Boy.
- Configured SQLite for testing.
- Integrated pytest-cov.
- Created application API and service tests.
- Configured GitHub Actions CI.
- Successfully passed 83 tests.
- Achieved 84% overall test coverage.

### Day 7 â€“ JWT Authentication and Advanced Testing

- Integrated Flask-JWT-Extended.
- Implemented user registration and login.
- Implemented access and refresh tokens.
- Configured token expiration.
- Implemented token blocklist.
- Added logout and token revocation.
- Protected application API routes.
- Created authentication test cases.

### Day 8 â€“ REST API Enhancement and Swagger Documentation

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

### Day 9 â€“ External Job Search API and Redis Caching

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

### Day 10 â€“ Email Notifications and Interview Reminders

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

### Day 11 â€“ CSV Import, Export and Bulk Updates

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
- Generate an error log for failed rows.

**3. Bulk Status Update**

- Update multiple application statuses using a CSV file.
- Validate application IDs and status values.
- Support statuses: APPLIED, PHONE_SCREEN, INTERVIEW, OFFER and REJECTED.
- Skip invalid records and generate an error log.

**API Endpoints**

- `GET /applications/export`
- `POST /applications/import`
- `POST /applications/bulk-status-update`

All three endpoints require JWT authentication.

**CSV Round-Trip Testing**

- Exported application records to CSV.
- Edited three application records.
- Re-imported the modified CSV.
- Verified updated roles and statuses through the applications API.
- Confirmed that existing records were updated without creating duplicates.
- Tested invalid rows and error log generation.

**Automated Testing**

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

### Day 12 â€“ Analytics Dashboard Backend

**1. Application Status History**

- Created `ApplicationStatusHistory` database model.
- Added application status history tracking.
- Stored status entry and exit timestamps.
- Recorded initial application status.
- Updated status history when an application status changes.
- Integrated status history tracking into application creation and updates.
- Added status history tracking to CSV import and bulk status update operations.
- Created and executed Alembic database migration.

Migration:

`70a60851e7bc_add_application_status_history_table.py`

**2. Response Rate Calculation**

Implemented response rate calculation:

`Response Rate = (Interview Applications / Total Applications) Ã— 100`

The API calculates the percentage of applications that reached the INTERVIEW status.

**3. Time-in-Stage Analysis**

- Calculates the average number of days spent in each application status.
- Uses status entry and exit timestamps.
- Tracks the current stage using the current time when no exit timestamp exists.
- Provides average duration for APPLIED, PHONE_SCREEN, INTERVIEW, OFFER and REJECTED statuses.

**4. Best Day to Apply**

- Analyzes application dates.
- Groups applications by weekday.
- Calculates the number of applications submitted on each weekday.
- Identifies the weekday with the highest number of applications.

**5. Application Analytics API**

Implemented an authenticated analytics endpoint:

`GET /api/analytics`

The endpoint returns:

- `total_applications`
- `response_rate`
- `average_days_per_status`
- `best_day_to_apply`
- `weekday_application_counts`
- `status_distribution`

**6. Seed Data and Manual Verification**

- Created 50 sample job applications.
- Generated varied application dates and statuses.
- Created corresponding application status history records.
- Verified analytics calculations using Postman.

**Sample Analytics Results**

| Metric | Result |
|---|---:|
| Total Applications | 53 |
| Interview Applications | 12 |
| Response Rate | 22.64% |
| Best Day to Apply | Monday |

Status distribution:

| Status | Applications |
|---|---:|
| APPLIED | 22 |
| PHONE_SCREEN | 10 |
| INTERVIEW | 12 |
| OFFER | 4 |
| REJECTED | 5 |

**7. Automated Testing**

Added `tests/test_analytics_api.py`.

Test coverage includes:
- Total application count.
- Response rate calculation.
- Average days per status.
- Status distribution.
- Best weekday to apply.
- Analytics API response validation.

**Final Test Results â€“ Day 12**

- Total tests passed: 101
- Failed tests: 0
- Execution time: 2.21 seconds

**Day 12 Deliverable**

Completed the application analytics API, status history tracking, analytics calculations, database migration, sample data verification, and automated testing.

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

### CSV APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications/export` | Export applications as CSV |
| POST | `/applications/import` | Import applications using CSV |
| POST | `/applications/bulk-status-update` | Update multiple application statuses |

### Analytics API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics` | Retrieve application analytics |

All protected endpoints require JWT authentication.

---

## Project Structure

```text
Job-Application-Tracker/
â”‚
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â””â”€â”€ tests.yml
â”‚
â”œâ”€â”€ api/
â”œâ”€â”€ auth/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â””â”€â”€ routes.py
â”‚
â”œâ”€â”€ migrations/
â”‚   â””â”€â”€ versions/
â”‚       â”œâ”€â”€ 70a60851e7bc_add_application_status_history_table.py
â”‚       â””â”€â”€ ...
â”‚
â”œâ”€â”€ models/
â”œâ”€â”€ schemas/
â”‚   â””â”€â”€ job_suggestion.py
â”‚
â”œâ”€â”€ services/
â”‚   â”œâ”€â”€ application_service.py
â”‚   â”œâ”€â”€ job_search_service.py
â”‚   â”œâ”€â”€ email_service.py
â”‚   â””â”€â”€ scheduler_service.py
â”‚
â”œâ”€â”€ templates/
â”‚   â””â”€â”€ emails/
â”‚       â”œâ”€â”€ weekly_digest.html
â”‚       â””â”€â”€ interview_reminder.html
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ conftest.py
â”‚   â”œâ”€â”€ factories.py
â”‚   â”œâ”€â”€ test_auth.py
â”‚   â”œâ”€â”€ test_application_api.py
â”‚   â”œâ”€â”€ test_application_service.py
â”‚   â”œâ”€â”€ test_file_upload.py
â”‚   â”œâ”€â”€ test_csv_api.py
â”‚   â”œâ”€â”€ test_analytics_api.py
â”‚   â””â”€â”€ test_helpers.py
â”‚
â”œâ”€â”€ postman/
â”œâ”€â”€ uploads/
â”‚
â”œâ”€â”€ app.py
â”œâ”€â”€ seed.py
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .coveragerc
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
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

## Running the Application

Start the required Docker services:

```bash
docker compose up -d
```

Apply database migrations:

```bash
flask --app app db upgrade
```

Run the Flask application:

```bash
python app.py
```

Open the API:

`http://127.0.0.1:5000`

Swagger documentation:

`http://127.0.0.1:5000/openapi/swagger`

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

Run CSV API tests:

```bash
pytest tests/test_csv_api.py -v
```

Run analytics API tests:

```bash
pytest tests/test_analytics_api.py -v
```

### Latest Test Results â€“ Day 12

| Metric | Result |
|---|---:|
| Total Tests Passed | 101 |
| Tests Failed | 0 |
| Execution Time | 2.21 seconds |
| Analytics API Test | Passed |
| CSV API Tests | Passed |
| Authentication Tests | Passed |
| Application API Tests | Passed |

Historical Day 6 coverage:
- Overall coverage: 84%
- app.py coverage: 85%
- Application Service coverage: 82%

Day 11 application code coverage: 81%.

---

## Current Project Status

**Completed Development: Day 1 - Day 13**

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
- CSV import and export.
- Bulk application status updates.
- Application status history tracking.
- Application analytics API.
- Response rate calculation.
- Time-in-stage analysis.
- Best weekday to apply analysis.
- Pytest automated testing.
- GitHub Actions CI.
- Flask-Mail SMTP integration.
- Weekly application digest emails.
- Interview scheduling model.
- Automated interview reminders.
- Jinja2 HTML email templates.
- APScheduler background jobs.

### Latest Project Verification

**109 Tests Passed | 0 Failed**

### Latest GitHub Commit

- Commit ID: `c7cefcd`
- Commit Message: `Complete Day 12 analytics dashboard API`
- Branch: `main`

---

## Developer

**Prasanna P**

GitHub: https://github.com/Prasanna-20740

LinkedIn: https://www.linkedin.com/in/prasanna-p20/

Portfolio: https://prasanna-p.vercel.app/

---

Developed as a hands-on Python Flask SaaS project, focusing on backend development, REST API design, database management, authentication, external API integration, caching, email automation, analytics, automated testing, and CI/CD.


## Day 13 - Admin API & Role Management

### Features Implemented

**1. User Role Management**
- Added USER and ADMIN roles to the User model.
- Created and applied database migrations for user roles and audit logs.
- Assigned ADMIN privileges to the administrator account.

**2. Admin Authorization**
- Implemented the `@admin_required` decorator.
- Protected administrator-only endpoints using JWT authentication and role verification.
- Restricted `GET /users` to administrators.

**3. Admin User Management**
- Implemented administrator user deletion.
- Prevented administrators from deleting their own accounts.
- Prevented deletion of the last administrator.
- Implemented user impersonation with dedicated JWT claims.

### Admin API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | List all users (Admin only) |
| DELETE | `/admin/users/<user_id>` | Delete a user (Admin only) |
| POST | `/admin/users/<user_id>/impersonate` | Impersonate a user (Admin only) |

### Audit Logging

- Created the `AuditLog` model and `record_audit()` helper.
- Recorded user deletion and impersonation actions.
- Stored administrator, target user, action and timestamp details.
- Preserved audit records after user deletion.

### Automated Testing

Added `tests/test_admin_api.py` with 7 tests covering:
- Admin authorization.
- User deletion and related record cleanup.
- Self-deletion prevention.
- Missing user handling.
- User impersonation.
- Impersonation authorization restrictions.
- Audit log verification.

**Day 13 Full Test Results:**
- 109 tests passed.
- 0 tests failed.

### Day 13 Deliverable

Completed administrator role management, secured admin APIs, user impersonation, account deletion and audit logging.


## Day 14 – Webhooks & Integrations

### Features Implemented

**1. Outbound Webhooks**
- Triggered webhook events when an application status changes.
- Stored webhook delivery details in the database.

**2. HMAC Security**
- Implemented HMAC-SHA256 signature generation.
- Added signature verification to validate webhook messages.
- Rejected invalid signatures.

**3. Slack Integration**
- Integrated Slack using Incoming Webhooks.
- Automatically sends a Slack notification when an application status changes to OFFER.

**4. Retry Mechanism**
- Implemented automatic retries for failed webhook deliveries.
- Configured a maximum of 3 retries.
- Marks delivery as FAILED after all retry attempts fail.

**5. Background Scheduler**
- Integrated APScheduler to process pending webhook deliveries automatically.
- Runs webhook delivery processing in the background.

**6. Webhook Delivery Tracking**
- Created the `WebhookDelivery` database model.
- Tracks PENDING, PROCESSING, DELIVERED and FAILED statuses.
- Stores delivery attempts and error details.

### Automated Testing

Added `tests/test_webhook_service.py` with 10 tests covering:
- HMAC signature generation.
- Valid and invalid signature verification.
- Webhook event creation.
- Slack notification queueing.
- Successful webhook delivery.
- Failed delivery and retry scheduling.
- Maximum retry limit.

**Day 14 Full Test Results:**
- 119 tests passed.
- 0 tests failed.

### Day 14 Deliverable

Completed webhook integration, HMAC security, Slack notifications, automatic retry handling, background scheduling and webhook delivery tracking.

