# Job Application Tracker SaaS

A Flask-based Job Application Tracker that helps users manage job applications, track application statuses, upload resumes, and extract skills from PDF resumes.

## 🚀 Project Overview

The Job Application Tracker is a backend application developed using Python, Flask, PostgreSQL, and SQLAlchemy.

It provides REST APIs to create, view, update, and delete job applications. It also supports resume uploads, PDF text extraction, and basic skill detection.

## 🛠️ Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Docker
- Flask-Migrate
- Alembic
- Postman
- PyPDF2
- Werkzeug
- Git and GitHub

## ✨ Features

### 1. Job Application Management
- Create a new job application.
- View all job applications.
- View an application by ID.
- Update application details.
- Delete a job application.

### 2. Application Status Tracking

Supported statuses:

- APPLIED
- PHONE_SCREEN
- INTERVIEW
- OFFER
- REJECTED

### 3. Resume Management
- Upload PDF resumes.
- Secure uploaded filenames.
- Maximum upload size: 5 MB.
- Store resume paths in PostgreSQL.
- Access uploaded resumes through an API.
- Automatically delete the resume when its application is deleted.

### 4. Resume Parsing
- Extract text from PDF resumes using PyPDF2.
- Identify skills using keyword matching.
- Return extracted text and detected skills through an API.

### 5. Backend Architecture
- SQLAlchemy database models.
- Service layer for application business logic.
- Custom exception handling.
- Application logging.
- Database migrations using Flask-Migrate and Alembic.

## 📁 Project Structure

```text
Job-Application-Tracker/
│
├── app.py
├── services/
│   └── application_service.py
│
├── migrations/
│
├── uploads/
│
├── .venv/
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.x
- Docker Desktop
- PostgreSQL
- Git
- Postman

### Step 1: Clone the Repository

```bash
git clone https://github.com/Prasanna-20740/Job-Application-Tracker.git
```

```bash
cd Job-Application-Tracker
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start PostgreSQL Using Docker

Ensure your PostgreSQL Docker container is running.

Database configuration currently used in the project:

```text
Database: job_tracker
Username: postgres
Password: postgres123
Host: localhost
Port: 5434
```

### Step 5: Apply Database Migrations

```bash
flask db upgrade
```

### Step 6: Run the Flask Application

```bash
python app.py
```

The application runs at:

```text
http://127.0.0.1:5000
```

## 🔗 API Endpoints

Base URL:

```text
http://127.0.0.1:5000
```

| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications` | Get all applications |
| POST | `/applications` | Create an application |
| GET | `/applications/<id>` | Get application by ID |
| PUT | `/applications/<id>` | Update an application |
| DELETE | `/applications/<id>` | Delete an application |
| POST | `/applications/<id>/resume` | Upload a resume |
| GET | `/files/<filename>` | Access an uploaded file |
| GET | `/applications/<id>/resume/skills` | Extract resume text and skills |

## 📄 Resume Upload API

**Method:** POST

```text
/applications/2/resume
```

Use Postman:

1. Select POST method.
2. Enter the resume upload URL.
3. Select Body → form-data.
4. Add a key named `file`.
5. Change the key type to File.
6. Select a PDF resume.
7. Click Send.

## 🧠 Resume Skills Extraction API

**Method:** GET

```text
/applications/2/resume/skills
```

Example response:

```json
{
    "application_id": 2,
    "extracted_text": "Resume content extracted from PDF",
    "skills": [
        "React",
        "HTML",
        "CSS",
        "MongoDB"
    ]
}
```

The extracted skills depend on the contents of the uploaded PDF and the configured keyword list.

## 🗄️ Database Models

### User Model

Stores user information:

- id
- username
- email

### JobApplication Model

Stores job application information:

- id
- company
- role
- status
- applied_date
- notes
- user_id
- resume_path

## 🧪 API Testing

All REST API endpoints can be tested using Postman.

Tested operations include:

- GET applications
- POST application
- GET application by ID
- PUT application
