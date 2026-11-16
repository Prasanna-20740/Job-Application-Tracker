# Job Application Tracker SaaS

A Python Flask-based Job Application Tracker SaaS designed to help users manage job applications, track application progress, upload resumes, extract skills from PDF resumes, and discover external job opportunities.

The application provides secure JWT authentication, RESTful API development, PostgreSQL database integration, automated testing, CI/CD automation, API documentation, external job search integration, and Redis caching.

---

# Tech Stack

### Backend
- Python
- Flask
- Flask-OpenAPI3

### Frontend / API Interface
- Swagger UI
- Postman

### Database
- PostgreSQL
- SQLite (Testing)

### ORM & Database Migrations
- Flask-SQLAlchemy
- Flask-Migrate
- Alembic

### Validation & Serialization
- Marshmallow
- Pydantic

### Authentication & Security
- JWT (JSON Web Tokens)
- Flask-JWT-Extended
- Token Blocklist
- Protected API Routes

### PDF Processing
- PyPDF2
- PDF Text Extraction
- Resume Skill Extraction

### External API Integration
- Adzuna Job Search API
- Python Requests

### Caching
- Redis
- Flask-Caching

### Testing
- Pytest
- Factory Boy
- Pytest-Cov

### DevOps & Tools
- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
- VS Code
- Postman

---

# Project Development Progress

## Day 1 – Project Setup & Architecture

### Project Planning
- Defined the Job Application Tracker SaaS use case.
- Identified the main application features and requirements.
- Planned a modular Flask backend architecture.
- Identified the database entities and relationships.

### Development Environment
- Installed and configured Python.
- Created a Python virtual environment using `venv`.
- Installed Flask.
- Installed Flask-SQLAlchemy.
- Configured PostgreSQL using Docker.
- Configured Docker Compose for database management.
- Initialized the Git repository.
- Created the initial project structure.

### Project Structure Setup
Created the initial folders:

- `api/` – API-related modules.
- `models/` – Database models.
- `services/` – Business logic.
- `tests/` – Automated tests.

---

## Day 2 – Database Design & Models

### PostgreSQL Integration
- Connected Flask application with PostgreSQL.
- Configured SQLAlchemy database connection.
- Integrated Flask-Migrate.
- Configured Alembic for database schema migrations.
- Created the initial database migration.

### JobApplication Model
Created the JobApplication database model with the following fields:

- ID
- Company
- Role
- Status
- Applied Date
- Notes
- User ID
- Resume Path

### Application Status Management

Created an `ApplicationStatus` enum with:

- `APPLIED`
- `PHONE_SCREEN`
- `INTERVIEW`
- `OFFER`
- `REJECTED`

### User Model
- Created the User database model.
- Added user-related fields.
- Designed the relationship between users and job applications.
- Prepared the database architecture for multi-user support.

---

## Day 3 – REST API Development

### Flask REST API
- Implemented RESTful API endpoints using Flask.
- Organized application routes.
- Implemented CRUD operations for job applications.

### Application CRUD Operations

**Create Application**
- Created API to add new job applications.
- Added company, role, status, applied date, and notes.
- Connected API requests with PostgreSQL.

**Get Applications**
- Implemented API to retrieve job applications.
- Added application listing functionality.

**Get Application by ID**
- Implemented API to retrieve a specific application.
- Added application ID-based lookup.

**Update Application**
- Implemented application update functionality.
- Added support for updating application details and status.

**Delete Application**
- Implemented application deletion functionality.

### Additional API Features
- Added request data validation.
- Implemented structured error handling.
- Added user management endpoints.
- Handled invalid application IDs.
- Improved API response consistency.

---

## Day 4 – Resume Upload & PDF Processing

### Resume Upload
- Implemented PDF resume upload functionality.
- Created resume upload API endpoint.
- Configured resume file storage.
- Added file type validation.
- Added PDF signature validation.
- Configured maximum upload size restrictions.
- Implemented resume file path management.

### PDF Processing
- Integrated PyPDF2 for PDF processing.
- Extracted text from uploaded PDF resumes.
- Implemented resume text processing.
- Added basic skill extraction functionality.

### Resume Skills API
- Created API endpoint to extract skills from uploaded resumes.
- Connected PDF processing with the application workflow.
- Added validation for uploaded resume files.
- Improved file upload error handling.

---

## Day 5 – Service Layer & Business Logic

### ApplicationService Implementation
- Created a dedicated `ApplicationService`.
- Separated business logic from Flask API routes.
- Implemented service-layer architecture.
- Improved code reusability and maintainability.

### Business Operations
Implemented service methods for:

- Creating job applications.
- Retrieving all applications.
- Retrieving applications by ID.
- Updating application details.
- Deleting applications.
- Listing user applications.

### Custom Exception Handling
Created custom exceptions:

- `ApplicationNotFound`
- `DuplicateApplication`

### Additional Improvements
- Implemented duplicate application handling.
- Improved database interaction.
- Added service-level error handling.
- Organized business logic into reusable functions.
- Improved project maintainability.

---

## Day 6 – Pytest Testing & GitHub Actions CI

### Pytest Configuration
- Installed and configured Pytest.
- Created `tests/` directory.
- Configured reusable fixtures using `conftest.py`.
- Integrated Factory Boy for test data generation.
- Configured SQLite for isolated test execution.
- Integrated pytest-cov for code coverage reporting.

### Automated Test Cases

Created and implemented test coverage for:

- Application Service.
- Application API.
- File Upload.
- Helper Functions.
- Application creation.
- Application retrieval.
- Application updates.
- Application deletion.
- Error handling.
- Validation scenarios.

### Test Configuration
- Created reusable test fixtures.
- Configured test database isolation.
- Added coverage reporting.
- Created `.coveragerc`.
- Added `.gitignore`.

### Test Results

- Successfully passed 83 automated tests.
- Achieved 84% overall test coverage.
- Achieved 85% app.py coverage.
- Achieved 82% Application Service coverage.

### GitHub Actions CI
- Created GitHub Actions workflow.
- Configured automated test execution.
- Automated testing on push events.
- Automated testing on pull requests.
- Verified workflow execution.
- Successfully achieved a green CI check.

---

## Day 7 – JWT Authentication & Advanced Testing

### JWT Authentication
- Installed Flask-JWT-Extended.
- Implemented JWT-based authentication.
- Created a dedicated `auth/` package.
- Implemented user registration.
- Implemented user login.
- Added JWT access token generation.
- Added JWT refresh token generation.
- Configured access token expiration.
- Configured refresh token expiration.

### Token Security
- Implemented JWT token validation.
- Created token blocklist functionality.
- Implemented token revocation during logout.
- Added protected API endpoints.
- Integrated authentication with application routes.
- Restricted access to protected resources.

### Database Migration
- Added authentication-related database changes.
- Created Alembic migration for token blocklist support.
- Applied database migration successfully.

### Authentication Testing
- Created `tests/test_auth.py`.
- Added registration test cases.
- Added login test cases.
- Added token validation test cases.
- Added refresh token test cases.
- Added logout and token revocation test cases.

### Advanced Testing Improvements
- Expanded application API test coverage.
- Improved file upload test cases.
- Updated reusable fixtures in `tests/conftest.py`.
- Updated dependencies in `requirements.txt`.
- Validated Python code using `py_compile`.
- Executed automated tests using Pytest.

### Git & GitHub
- Committed Day 7 changes.
- Resolved Git synchronization issues.
- Used Git rebase to synchronize local and remote changes.
- Successfully pushed Day 7 implementation to GitHub.

---

## Day 8 – REST API Enhancement & Swagger Documentation

### Flask-OpenAPI3 Integration
- Installed Flask-OpenAPI3.
- Integrated OpenAPI specification with Flask.
- Configured Swagger UI.
- Added interactive API documentation.
- Documented API request and response schemas.

### API Documentation
Configured Swagger UI at:

`http://127.0.0.1:5000/openapi/swagger`

### Application API Enhancements

Implemented and documented:

- `GET /applications`
- `POST /applications`
- `GET /applications/stats`
- `GET /applications/{application_id}`
- `PATCH /applications/{application_id}`
- `DELETE /applications/{application_id}`

### Pagination
- Implemented pagination for application listing.
- Added page and per-page parameters.
- Added total application count.
- Added pagination response headers.

Implemented headers:

- `X-Total-Count`
- `X-Page`
- `X-Per-Page`
- `X-Total-Pages`

### Application Statistics
- Implemented application statistics endpoint.
- Added application status summary functionality.
- Enabled retrieval of application statistics through REST API.

### API Testing
- Created Postman collection.
- Added API request examples.
- Tested application CRUD endpoints.
- Tested application statistics.
- Tested pagination.
- Verified API response status codes.
- Fixed validation response expectations.
- Corrected update method implementation from PUT to PATCH where required.
- Successfully executed automated test suite.

### GitHub
- Committed Day 8 REST API enhancements.
- Resolved Git rebase synchronization.
- Successfully pushed Day 8 changes to GitHub.

---

## Day 9 – External Job Search API Integration & Redis Caching

### Adzuna Job Search API Integration
- Registered for the Adzuna Developer API.
- Integrated Adzuna external job search API.
- Configured API credentials using environment variables.
- Used Python Requests to communicate with the external API.
- Created a dedicated job search service.

### JobSearchService
Created:

`services/job_search_service.py`

Implemented:

- External API communication.
- Keyword-based job search.
- Location-based job search.
- Job result processing.
- Company information extraction.
- Salary information extraction.
- Job location extraction.
- Job description extraction.
- External job application redirect URL retrieval.
- API timeout handling.
- External API error handling.
- Logging for job search requests.

### JobSuggestion DTO
Created:

`schemas/job_suggestion.py`

Implemented Pydantic-based job response validation.

Job response fields include:

- Job Title
- Company
- Location
- Minimum Salary
- Maximum Salary
- Redirect URL
- Description

### External Job Search API

Implemented endpoint:

`GET /api/jobs/search`

Example request:

`/api/jobs/search?q=python&location=chennai`

Features:

- Search jobs using keywords.
- Filter jobs by location.
- Retrieve external job listings.
- Return structured JSON responses.
- Validate external API response data.
- Handle API configuration errors.
- Handle external service failures.

### Redis Integration
- Installed Redis Python client.
- Integrated Flask-Caching.
- Configured Redis as the caching backend.
- Added Redis service to Docker Compose.
- Started Redis container successfully.
- Verified Redis connectivity using Redis CLI.

Redis connection:

`redis://localhost:6379/0`

### Redis Caching Implementation
- Implemented job search result caching.
- Created keyword and location-based cache keys.
- Added cache hit detection.
- Added cache miss detection.
- Configured cache expiration to 30 minutes.
- Stored validated job search results in Redis.
- Reduced repeated external API requests.

### Cache Verification

**First Request:**
- Fetches job results from Adzuna API.
- Returns `source: adzuna_api`.
- Stores results in Redis.

**Subsequent Request:**
- Retrieves cached results from Redis.
- Returns `source: cache`.
- Avoids another external API request while the cache is valid.

### Environment Configuration
- Integrated python-dotenv.
- Loaded API credentials from `.env`.
- Used environment variables for API configuration.
- Avoided hardcoding credentials in application code.

### API Testing
- Started Flask application successfully.
- Tested job search through Swagger UI.
- Searched for Python jobs in Chennai.
- Successfully retrieved five job results.
- Verified job titles, company names, locations, salary details, and redirect URLs.
- Verified Redis cache hit on repeated requests.
- Executed Python syntax validation using `py_compile`.

### Automated Testing
Executed:

`pytest -q`

Final result:

- **92 tests passed**
- **0 tests failed**
- Adzuna API integration verified.
- Redis caching verified.
- Existing automated test suite passed.

---

# API Endpoints

## Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and generate tokens |
| POST | `/auth/refresh` | Generate a new access token |
| POST | `/auth/logout` | Revoke authentication token |

## Job Application APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications` | Retrieve applications with pagination |
| POST | `/applications` | Create a new application |
| GET | `/applications/stats` | Retrieve application statistics |
| GET | `/applications/{application_id}` | Retrieve application by ID |
| PATCH | `/applications/{application_id}` | Update application |
| DELETE | `/applications/{application_id}` | Delete application |

## Resume APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/applications/{application_id}/resume` | Upload PDF resume |
| GET | `/applications/{application_id}/skills` | Extract skills from uploaded resume |
| GET | `/files/{filename}` | Access uploaded file where supported |

## External Job Search API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs/search` | Search external jobs using Adzuna |

Example:

`GET /api/jobs/search?q=python&location=chennai`

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
│
├── auth/
│   ├── __init__.py
│   └── routes.py
│
├── migrations/
│   └── versions/
│
├── models/
│
├── schemas/
│   └── job_suggestion.py
│
├── services/
│   └── job_search_service.py
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
│
├── app.py
├── seed.py
├── docker-compose.yml
├── requirements.txt
├── .coveragerc
├── .gitignore
├── .env
└── README.md
```

---

# Running the Project Locally

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

Create a `.env` file in the project root.

Example:

```env
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

REDIS_URL=redis://localhost:6379/0
```

Configure the PostgreSQL database connection using the database settings expected by the application.

**Security:** Never commit `.env` or real API credentials to GitHub. Use placeholder values in `.env.example`.

## 6. Start PostgreSQL and Redis

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

## 7. Run Database Migrations

```bash
flask db upgrade
```

## 8. Start Flask Application

```bash
python app.py
```

Application URL:

`http://127.0.0.1:5000`

Swagger UI:

`http://127.0.0.1:5000/openapi/swagger`

---

# Running Automated Tests

Run all tests:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov=services --cov-report=term-missing
```

Run authentication tests:

```bash
pytest tests/test_auth.py -v
```

---

# Test Results

| Metric | Result |
|---|---:|
| Day 6 Tests Passed | 83 |
| Day 6 Overall Coverage | 84% |
| Day 6 app.py Coverage | 85% |
| Day 6 Application Service Coverage | 82% |
| GitHub Actions CI | Passed |
| Latest Day 9 Tests Passed | 92 |
| Latest Day 9 Tests Failed | 0 |
| Adzuna API Integration | Verified |
| Redis Caching | Verified |
| Swagger API Documentation | Implemented |

*Day 6 coverage metrics are historical. The Day 9 result represents the latest successful test execution.*

---

# GitHub Repository

**Repository:**  
https://github.com/Prasanna-20740/Job-Application-Tracker

---

# Current Project Status

**Completed Development:** Day 1 – Day 9

### Major Features Completed

- Flask application architecture.
- PostgreSQL database integration.
- SQLAlchemy database models.
- Alembic database migrations.
- RESTful CRUD APIs.
- Multi-user database structure.
- Resume upload functionality.
- PDF text extraction.
- Resume skill extraction.
- Service-layer architecture.
- Custom exception handling.
- JWT authentication.
- Access and refresh tokens.
- Token blocklist and logout functionality.
- Automated testing with Pytest.
- Factory Boy test data generation.
- Test coverage reporting.
- GitHub Actions CI.
- Swagger API documentation.
- Application pagination.
- Application statistics.
- Postman API collection.
- Adzuna external job search.
- Pydantic DTO validation.
- Redis caching.
- Docker-based PostgreSQL and Redis services.

### Latest Test Execution

**92 Passed | 0 Failed**

---

Developed as a hands-on Python Flask SaaS project, with a focus on backend development, REST API design, database management, authentication, external API integration, caching, automated testing, and CI/CD.
