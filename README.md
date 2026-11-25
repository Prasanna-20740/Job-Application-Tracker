# Job Application Tracker SaaS

A Python Flask-based Job Application Tracker SaaS designed to help users manage job applications, track application progress, upload and analyze resumes, discover external job opportunities, monitor application analytics, and manage interview schedules.

The application follows a modular backend architecture and includes secure authentication, RESTful APIs, database management, external integrations, automated notifications, background jobs, and comprehensive testing.

**GitHub Repository:** https://github.com/Prasanna-20740/Job-Application-Tracker

---

## Table of Contents

- Overview
- Features
- Technology Stack
- Project Development Progress (Day 1–Day 16)
- API Endpoints
- Project Structure
- Installation and Setup
- Environment Configuration
- Running the Application
- Email Notification System
- Security Implementation
- Automated Testing
- Project Status
- Developer

---

## Overview

The Job Application Tracker helps users maintain job application records, monitor application statuses, upload resumes, review extracted skills, analyze application progress, and receive automated reminders.

## Features

- User registration and login using JWT authentication.
- Access token and refresh token management.
- Job application CRUD operations.
- Application status tracking and history.
- PDF resume upload, text extraction, and skill extraction.
- Asynchronous resume parsing using Celery.
- Application statistics, pagination, and analytics.
- External job search using Adzuna API.
- Redis caching for job search results and rate limiting.
- Interactive Swagger API documentation and Postman collection.
- CSV import, export, and bulk application status updates.
- Weekly job application digest emails.
- Automated interview reminder emails.
- Admin role management, protected admin APIs, user impersonation, and audit logging.
- Outbound webhooks with HMAC-SHA256 signature verification.
- Slack notifications and automatic webhook retries.
- API rate limiting, security headers, input sanitization, and restricted CORS.
- Scheduled stale application email alerts using Celery Beat.
- Background task monitoring using Flower.
- Automated testing using Pytest and CI using GitHub Actions.

---

## Technology Stack

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
- JWT
- Flask-JWT-Extended
- Token Blocklist
- Flask-Limiter
- Flask-Talisman
- Flask-CORS
- nh3

### Validation and Serialization
- Marshmallow
- Pydantic

### External Integrations
- Adzuna Job Search API
- Slack Incoming Webhooks
- Python Requests

### Caching and Background Processing
- Redis
- Flask-Caching
- Celery
- Celery Beat
- Flower

### Email and Scheduling
- Flask-Mail
- Mailtrap SMTP
- Jinja2
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
- Postman
- Git and GitHub

---

# Project Development Progress

## Day 1 – Project Setup and Architecture
- Planned the Job Application Tracker SaaS.
- Identified project requirements and core features.
- Designed a modular Flask backend architecture.
- Created a Python virtual environment.
- Installed Flask and Flask-SQLAlchemy.
- Configured PostgreSQL using Docker.
- Initialized Git and the GitHub repository.

**Deliverable:** Initial project setup and backend architecture.

## Day 2 – Database Design and Models
- Integrated PostgreSQL with Flask.
- Configured SQLAlchemy ORM.
- Integrated Flask-Migrate and Alembic.
- Created the `JobApplication` and `User` models.
- Implemented application status using Python Enum.
- Designed user and application relationships.

**Deliverable:** Database models and migration setup.

## Day 3 – REST API Development
- Implemented RESTful APIs.
- Developed application CRUD operations.
- Implemented application creation, retrieval, updating, and deletion.
- Added request validation and structured error handling.
- Added user management endpoints.

**Deliverable:** Core application management APIs.

## Day 4 – Resume Upload and PDF Processing
- Implemented PDF resume upload.
- Added file type and PDF signature validation.
- Configured file storage.
- Integrated PyPDF2 for PDF text extraction.
- Developed basic resume skill extraction.
- Created resume-related API endpoints.

**Deliverable:** Resume upload and PDF processing functionality.

## Day 5 – Service Layer and Business Logic
- Created `ApplicationService`.
- Separated business logic from API routes.
- Implemented reusable service methods.
- Added custom exceptions: `ApplicationNotFound` and `DuplicateApplication`.
- Improved error handling and code organization.

**Deliverable:** Modular service-layer architecture.

## Day 6 – Pytest and GitHub Actions CI
- Configured Pytest and reusable test fixtures.
- Integrated Factory Boy.
- Configured SQLite for testing.
- Integrated pytest-cov.
- Created application API and service tests.
- Configured GitHub Actions CI.
- Successfully passed 83 tests.
- Achieved 84% overall test coverage at this stage.

**Deliverable:** Automated testing and CI workflow.

## Day 7 – JWT Authentication and Advanced Testing
- Integrated Flask-JWT-Extended.
- Implemented user registration and login.
- Implemented access and refresh tokens.
- Configured token expiration.
- Implemented token blocklist, logout, and token revocation.
- Protected application API routes.
- Created authentication test cases.

**Deliverable:** Secure JWT authentication system.

## Day 8 – REST API Enhancement and Swagger Documentation
- Integrated Flask-OpenAPI3.
- Configured Swagger UI and documented REST API endpoints.
- Implemented application pagination and statistics.
- Added pagination response headers.
- Created a Postman collection.
- Tested CRUD operations and API responses.

**Swagger UI:** `http://127.0.0.1:5000/openapi/swagger`

**Deliverable:** Documented and enhanced REST API.

## Day 9 – External Job Search API and Redis Caching

### Adzuna API Integration
- Integrated Adzuna Job Search API.
- Configured API credentials using environment variables.
- Implemented keyword-based and location-based job search.
- Created `JobSearchService` and Pydantic `JobSuggestion` DTO.
- Added external API error handling.

### Redis Integration
- Integrated Redis with Flask and Docker Compose.
- Implemented job search result caching.
- Configured 30-minute cache expiration.
- Implemented cache hit and cache miss detection.

**API Example:** `GET /api/jobs/search?q=python&location=chennai`

**Deliverable:** External job search and Redis caching.

## Day 10 – Email Notifications and Interview Reminders

### Email Integration
- Integrated Flask-Mail.
- Configured Mailtrap Email Sandbox.
- Configured SMTP credentials using environment variables.
- Verified email delivery through Mailtrap.

### Weekly Job Application Digest
- Retrieves applications updated during the previous seven days.
- Generates a weekly application summary.
- Displays company, role, and application status.
- Sends digest emails to registered users.
- Configured weekly scheduling for Monday at 9:00 AM.

### Interview Scheduling
- Created the Interview database model and linked interviews with job applications.
- Added interview date, time, type, meeting link, and notes.
- Implemented automatic interview reminder emails.
- Checks upcoming interviews every five minutes.
- Sends reminders approximately 24 hours before interviews.
- Uses `reminder_sent` to prevent duplicate reminders.

### HTML Email Templates
- `templates/emails/weekly_digest.html`
- `templates/emails/interview_reminder.html`

**Deliverable:** Automated email notifications and interview reminders.

## Day 11 – CSV Import, Export and Bulk Updates

### CSV Export
- Exported applications belonging to the authenticated user.
- Downloaded application records as CSV.
- Included ID, company, role, status, applied date, and notes.
- Protected user data using JWT authentication and user-level filtering.

### CSV Import
- Implemented application import using CSV files.
- Validated required CSV headers and application fields.
- Created new applications when ID was empty.
- Updated existing applications using application ID.
- Skipped invalid rows and generated error logs.

### Bulk Status Update
- Implemented bulk application status updates.
- Validated application IDs and status values.
- Supported APPLIED, PHONE_SCREEN, INTERVIEW, OFFER, and REJECTED statuses.

### API Endpoints
- `GET /applications/export`
- `POST /applications/import`
- `POST /applications/bulk-status-update`

Added `tests/test_csv_api.py` with eight automated tests.

**Deliverable:** CSV data management and bulk update functionality.

## Day 12 – Analytics Dashboard Backend

### Application Status History
- Created `ApplicationStatusHistory` database model.
- Added application status history tracking.
- Stored status entry and exit timestamps.
- Recorded initial application status.
- Updated status history when application status changed.
- Integrated history tracking into application creation, updates, CSV import, and bulk status updates.
- Created and executed Alembic database migration.

### Response Rate Calculation

`Response Rate = (Interview Applications / Total Applications) × 100`

The API calculates the percentage of applications that reached INTERVIEW status.

### Time-in-Stage Analysis
- Calculated average days spent in each application status.
- Used status entry and exit timestamps.
- Tracked the current stage using the current time when no exit timestamp existed.
- Provided average duration for APPLIED, PHONE_SCREEN, INTERVIEW, OFFER, and REJECTED statuses.

### Best Day to Apply
- Analyzed application dates and grouped applications by weekday.
- Calculated applications submitted on each weekday.
- Identified the weekday with the highest number of applications.

### Analytics API

`GET /api/analytics`

Returns:
- `total_applications`
- `response_rate`
- `average_days_per_status`
- `best_day_to_apply`
- `weekday_application_counts`
- `status_distribution`

**Deliverable:** Application analytics API and status history tracking.

## Day 13 – Admin API and Role Management

### User Role Management
- Added USER and ADMIN roles to the User model.
- Created and applied database migrations for user roles and audit logs.
- Assigned ADMIN privileges to the administrator account.

### Admin Authorization
- Implemented the `@admin_required` decorator.
- Protected administrator-only endpoints using JWT authentication and role verification.
- Restricted `GET /users` to administrators.

### Admin User Management
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
- Stored administrator, target user, action, and timestamp details.
- Preserved audit records after user deletion.

Added `tests/test_admin_api.py` with seven tests.

**Deliverable:** Admin role management, protected admin APIs, impersonation, and audit logging.

## Day 14 – Webhooks and Integrations

### Outbound Webhooks
- Triggered webhook events when an application status changed.
- Stored webhook delivery details in the database.

### HMAC Security
- Implemented HMAC-SHA256 signature generation.
- Added signature verification to validate webhook messages.
- Rejected invalid signatures.

### Slack Integration
- Integrated Slack using Incoming Webhooks.
- Automatically sends a Slack notification when an application status changes to OFFER.

### Retry Mechanism
- Implemented automatic retries for failed webhook deliveries.
- Configured a maximum of three retries.
- Marks delivery as FAILED after all retry attempts fail.

### Background Scheduler and Delivery Tracking
- Integrated APScheduler to process pending webhook deliveries automatically.
- Created the `WebhookDelivery` database model.
- Tracks PENDING, PROCESSING, DELIVERED, and FAILED statuses.
- Stores delivery attempts and error details.

Added `tests/test_webhook_service.py` with ten tests.

**Deliverable:** Webhook integration, HMAC security, Slack notifications, retry handling, and delivery tracking.

## Day 15 – Rate Limiting and Security

### API Rate Limiting
- Integrated Flask-Limiter.
- Configured Redis as the rate-limit storage backend.
- Implemented a limit of 100 requests per minute.
- Used authenticated user identity for rate-limit keys when a bearer token is available.
- Enabled rate-limit response headers.

### Security Headers
- Integrated Flask-Talisman.
- Configured `X-Frame-Options` as DENY.
- Configured `X-Content-Type-Options` as nosniff.
- Configured `Referrer-Policy` as strict-origin-when-cross-origin.
- Kept HTTPS enforcement disabled for local HTTP development.

### XSS Prevention
- Integrated nh3 for input sanitization.
- Created `services/security_service.py`.
- Implemented `sanitize_notes()`.
- Removed HTML tags and attributes from application notes.
- Applied sanitization during application creation and updates.
- Integrated sanitization into Marshmallow schema validation.

### CORS Configuration
- Integrated Flask-CORS.
- Restricted allowed frontend origin to `http://localhost:3000`.
- Configured permitted request methods and headers.
- Exposed rate-limit response headers.

### Security Testing
- Created `tests/test_security.py`.
- Tested normal text and HTML sanitization.
- Tested script and malicious image tag removal.
- Tested security headers and allowed/blocked CORS origins.
- Verified rate limiting: the first 100 requests succeeded and subsequent requests were rate-limited with HTTP 429.

**Deliverable:** API rate limiting, Redis-backed request tracking, security headers, XSS protection, CORS configuration, and security tests.

## Day 16 – Background Jobs and Asynchronous Processing

### Celery and Redis Integration
- Integrated Celery for asynchronous background task processing.
- Configured Redis as the message broker and task result backend.
- Added Flask application context support for Celery tasks.

### Asynchronous Resume Parsing
- Updated the resume upload workflow to trigger background processing.
- Implemented the `tasks.parse_resume` Celery task.
- Extracted text from uploaded PDF resumes.
- Automatically identified skills from extracted resume content.
- Saved extracted resume text and skills in PostgreSQL.
- Added resume parsing status and parsed timestamp tracking.

### Stale Application Alerts
- Implemented the `tasks.send_stale_application_alerts` task.
- Identifies applications that have not been updated for more than 14 days.
- Sends email reminders to users with eligible stale applications.
- Tracks alert delivery using the `stale_alert_sent_at` field to prevent repeated alerts.
- Excludes applications with OFFER and REJECTED statuses.

### Celery Beat Scheduling
- Configured Celery Beat for periodic background tasks.
- Scheduled stale application alerts to run daily at 9:00 AM.
- Configured the Asia/Kolkata timezone.

### Flower Monitoring
- Integrated Flower for Celery task monitoring.
- Monitored worker availability and task execution.
- Verified successful background task execution through the Flower dashboard.

### Verification and Testing
- Verified Redis connection and Celery worker availability.
- Successfully uploaded a PDF resume and verified asynchronous parsing through worker logs.
- Confirmed task execution status as SUCCESS in Flower.
- Verified extracted skills were saved in PostgreSQL.
- Confirmed resume parsing status as COMPLETED.
- Tested stale application alert task.
- **128 tests passed and 0 tests failed.**

**Deliverable:** Asynchronous resume parsing, Redis-backed Celery task processing, scheduled stale application email alerts, and Flower-based task monitoring.

---

# API Endpoints

## Authentication APIs
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | User login |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Revoke authentication token |

## Job Application APIs
| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications` | Retrieve applications with pagination |
| POST | `/applications` | Create application |
| GET | `/applications/stats` | Application statistics |
| GET | `/applications/{application_id}` | Retrieve application |
| PATCH | `/applications/{application_id}` | Update application |
| DELETE | `/applications/{application_id}` | Delete application |

## Resume APIs
| Method | Endpoint | Description |
|---|---|---|
| POST | `/applications/{application_id}/resume` | Upload PDF resume |
| GET | `/applications/{application_id}/skills` | Retrieve extracted resume skills |
| GET | `/files/{filename}` | Access uploaded file where supported |

## External Job Search API
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs/search` | Search external jobs using Adzuna |

## CSV APIs
| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications/export` | Export applications as CSV |
| POST | `/applications/import` | Import applications using CSV |
| POST | `/applications/bulk-status-update` | Update multiple application statuses |

## Analytics API
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics` | Retrieve application analytics |

## Admin APIs
| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | List users (Admin only) |
| DELETE | `/admin/users/<user_id>` | Delete user (Admin only) |
| POST | `/admin/users/<user_id>/impersonate` | Impersonate a user (Admin only) |

All protected endpoints require JWT authentication. Admin endpoints additionally require administrator authorization.

---

# Project Structure

```text
Job-Application-Tracker/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── api/
├── auth/
├── migrations/
│   └── versions/
├── models/
├── schemas/
├── services/
├── templates/
│   └── emails/
├── tests/
├── postman/
├── uploads/
│
├── app.py
├── run.py
├── celery_app.py
├── tasks.py
├── seed.py
├── docker-compose.yml
├── requirements.txt
├── .coveragerc
├── .gitignore
└── README.md
```

*Note: This is a representative project structure. Some folders and files may vary as the project evolves.*

---

# Installation and Setup

## Prerequisites
- Python 3.10+
- PostgreSQL
- Docker Desktop
- Redis
- Git

## 1. Clone Repository

```bash
git clone https://github.com/Prasanna-20740/Job-Application-Tracker.git
cd Job-Application-Tracker
```

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file in the project root and configure the required database, API, Redis, and email credentials.

## 6. Start PostgreSQL and Redis

```bash
docker compose up -d
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

## 7. Run Database Migrations

```bash
flask --app app db upgrade
```

## 8. Start Flask Application

```bash
python app.py
```

Application URL: `http://127.0.0.1:5000`

Swagger UI: `http://127.0.0.1:5000/openapi/swagger`

---

# Environment Configuration

Create a `.env` file in the project root.

Example placeholders:

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

# Running the Application

Start Docker services:

```bash
docker compose up -d
```

Apply database migrations:

```bash
flask --app app db upgrade
```

Start the Flask application:

```bash
python app.py
```

Start the Celery worker (Windows):

```bash
celery -A celery_app.celery worker --loglevel=info --pool=solo
```

Start Celery Beat:

```bash
celery -A celery_app.celery beat --loglevel=info
```

Start Flower monitoring:

```bash
celery -A celery_app.celery flower --port=5555
```

Flower Dashboard: `http://127.0.0.1:5555`

Run Flask, Celery worker, and Celery Beat in separate terminals. Start Flower in another terminal when task monitoring is required.

---

# Email Notification System

## Weekly Digest
- Runs every Monday at 9:00 AM.
- Retrieves applications updated during the previous seven days.
- Sends an HTML summary email with application details.

## Interview Reminder
- Scheduler checks every five minutes.
- Finds interviews approximately 24 hours before their scheduled time.
- Sends an HTML reminder email.
- Updates the `reminder_sent` database field after successful delivery.

## Stale Application Alert
- Celery Beat schedules the alert task daily at 9:00 AM (Asia/Kolkata).
- Finds applications that have not been updated for more than 14 days.
- Excludes OFFER and REJECTED applications.
- Uses `stale_alert_sent_at` to prevent duplicate alerts.

Mailtrap Email Sandbox was used to verify SMTP connectivity, weekly digest delivery, interview reminder delivery, Jinja2 dynamic content, and HTML email rendering.

---

# Security Implementation

| Security Feature | Implementation |
|---|---|
| Authentication | Flask-JWT-Extended |
| Token Revocation | JWT Token Blocklist |
| Role-Based Access | Admin Authorization |
| API Rate Limiting | Flask-Limiter and Redis |
| Security Headers | Flask-Talisman |
| Input Sanitization | nh3 |
| Cross-Origin Protection | Flask-CORS |
| Webhook Verification | HMAC-SHA256 |

The local development configuration uses HTTP. HTTPS enforcement should be configured appropriately when deploying to production.

---

# Automated Testing

Run all tests:

```bash
pytest -q
```

Run tests with coverage:

```bash
pytest --cov=app --cov=services --cov-report=term-missing
```

Run individual test modules:

```bash
pytest tests/test_auth.py -v
pytest tests/test_csv_api.py -v
pytest tests/test_analytics_api.py -v
pytest tests/test_admin_api.py -v
pytest tests/test_webhook_service.py -v
pytest tests/test_security.py -v
```

## Latest Test Results – Day 16

| Metric | Result |
|---|---:|
| Total Tests Passed | 128 |
| Tests Failed | 0 |
| Security Tests | Passed |
| Webhook Tests | Passed |
| Admin API Tests | Passed |
| Authentication Tests | Passed |
| Application API Tests | Passed |

The complete test suite passed successfully with 128 tests.

---

# Current Project Status

**Development Progress: Day 1 – Day 16 Completed**

### Major Milestones
- Modular Flask backend architecture.
- PostgreSQL database and SQLAlchemy ORM.
- RESTful CRUD APIs and Swagger documentation.
- PDF resume upload, text extraction, and skill extraction.
- Service-layer architecture and structured error handling.
- JWT authentication and token revocation.
- Redis caching and external job search.
- Automated email notifications and interview reminders.
- CSV import, export, and bulk updates.
- Application analytics and status history.
- Admin role management and audit logging.
- Webhook and Slack integration.
- HMAC signature verification and retry handling.
- API rate limiting and security hardening.
- Celery and Redis background task processing.
- Asynchronous resume parsing and scheduled stale application alerts.
- Flower task monitoring.
- Automated testing and GitHub Actions CI.

### Latest GitHub Commit

Update this section with the latest commit ID and message after pushing the README changes.

- **Branch:** `main`

---

# Developer

**Prasanna P**

- **GitHub:** https://github.com/Prasanna-20740
- **LinkedIn:** https://www.linkedin.com/in/prasanna-p20/
- **Portfolio:** https://prasanna-p.vercel.app/

---

Developed as a hands-on Python Flask SaaS project, focusing on backend development, REST API design, database management, authentication, external API integration, caching, email automation, analytics, webhooks, security implementation, background processing, automated testing, and CI/CD.
