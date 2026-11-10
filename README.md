# Job Application Tracker SaaS

A Flask-based backend application to manage and track job applications. This project provides REST APIs for creating, viewing, updating, and deleting job applications with PostgreSQL database integration, service-layer architecture, request validation, and standardized error handling.

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Docker
- Flask-Migrate
- Alembic
- Marshmallow
- Postman

---

## Project Features

### Day 1 – Project Setup and Database Connection

- Defined the Job Application Tracker SaaS use case.
- Created and configured Python virtual environment.
- Installed Flask and Flask-SQLAlchemy.
- Configured PostgreSQL using Docker.
- Connected Flask application with PostgreSQL.
- Created the initial project structure.

### Day 2 – Database Models and Migrations

- Created User model for multi-user support.
- Created JobApplication model.
- Implemented application fields:
  - ID
  - Company
  - Role
  - Status
  - Applied Date
  - Notes
  - User ID
- Implemented ApplicationStatus Enum:
  - APPLIED
  - PHONE_SCREEN
  - INTERVIEW
  - OFFER
  - REJECTED
- Established relationship between User and JobApplication.
- Configured Flask-Migrate and Alembic.
- Created and applied database migrations.

### Day 3 – Service Layer and CRUD Operations

- Implemented Application Service Layer.
- Separated business logic from API routes.
- Implemented CRUD operations:
  - Create application
  - Get all applications
  - Get application by ID
  - Update application
  - Delete application
- Implemented custom exceptions:
  - ApplicationNotFound
  - DuplicateApplication
- Added logging for application operations.
- Implemented duplicate application checking.
- Tested CRUD APIs using Postman.

### Day 4 – Request Validation and Error Handling

- Integrated Marshmallow for request data validation.
- Created ApplicationSchema for validating application data.
- Implemented company name validation (cannot be empty).
- Implemented applied date validation (cannot be in the future).
- Implemented application status validation.
- Integrated schema validation into POST and PUT APIs.
- Implemented standardized error response format:

```json
{
    "error": "Validation failed",
    "details": {},
    "status_code": 400
}
```

- Implemented Flask error handlers:
  - 400 – Bad Request
  - 404 – Resource Not Found
  - 413 – File Too Large
  - 500 – Internal Server Error
- Tested valid and invalid requests using Postman.

---

## API Endpoints

Base URL: `http://127.0.0.1:5000`

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | `/applications` | Create a new application |
| GET | `/applications` | Retrieve all applications |
| GET | `/applications/<application_id>` | Retrieve application by ID |
| PUT | `/applications/<application_id>` | Update an application |
| DELETE | `/applications/<application_id>` | Delete an application |

---

## Database Structure

**Database:** PostgreSQL

**Tables:**

### users

- id
- username
- email

### job_application

- id
- company
- role
- status
- applied_date
- notes
- user_id
- resume_path

Note: `resume_path` is included in the database model for the resume management functionality developed later.

---

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/Prasanna-20740/Job-Application-Tracker.git
```

```bash
cd Job-Application-Tracker
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start PostgreSQL

Start the configured PostgreSQL Docker container.

Ensure PostgreSQL is accessible through the configured database port.

### 6. Run database migrations

```bash
flask db upgrade
```

### 7. Start Flask application

```bash
python app.py
```

Application URL:

`http://127.0.0.1:5000`

---

## API Testing

Postman is used to test:

- Application creation
- Application retrieval
- Application updates
- Application deletion
- Duplicate application validation
- Invalid company name
- Future applied date
- Invalid application status
- Application not found responses

---

## Error Response Format

All standardized error responses use the following structure:

```json
{
    "error": "Error message",
    "details": {},
    "status_code": 400
}
```

---

## Future Enhancements

- JWT Authentication
- User authentication and authorization
- Dashboard and analytics
- Advanced job application tracking
- Improved resume skill extraction

---

## Repository

GitHub: https://github.com/Prasanna-20740/Job-Application-Tracker

## Author

**Prasanna**

---

## Project Progress

| Day | Description | Status |
|---|---|---|
| Day 1 | Project Setup and Database Connection | Completed |
| Day 2 | Database Models and Migrations | Completed |
| Day 3 | Service Layer and CRUD Operations | Completed |
| Day 4 | Marshmallow Validation and Error Handling | Completed |
| Day 5 | Resume Management | Upcoming in this README version |
