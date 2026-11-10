# Job Application Tracker

A Python Flask REST API project to manage job applications. This application allows users to create, view, update, and delete job application records using PostgreSQL as the database.

## 🚀 Project Overview

The Job Application Tracker helps users maintain their job application details, including company name, job role, and application status.

## 🛠️ Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Docker
- Postman
- Git & GitHub

## ✨ Features

- View all job applications
- Create a new job application
- Get application details by ID
- Update existing application details
- Delete job applications
- Input validation
- Error handling (400, 404, 500)
- PostgreSQL database integration

## 📁 Project Structure

```text
Job-Application-Tracker/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── docker-compose.yml
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Prasanna-20740/Job-Application-Tracker.git
```

### 2. Navigate to Project Folder

```bash
cd Job-Application-Tracker
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install flask flask-sqlalchemy psycopg2-binary
```

### 6. Start PostgreSQL Database

Make sure Docker Desktop is running.

```bash
docker compose up -d
```

The PostgreSQL database should be accessible through port `5434`.

### 7. Run Flask Application

```bash
python app.py
```

Server URL:

```text
http://127.0.0.1:5000
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home API |
| GET | `/applications` | Get all applications |
| POST | `/applications` | Create application |
| GET | `/applications/<id>` | Get application by ID |
| PUT | `/applications/<id>` | Update application |
| DELETE | `/applications/<id>` | Delete application |

## 🧪 API Testing

All APIs are tested using Postman.

### 1. Create Application – POST

**URL:**

```text
POST http://127.0.0.1:5000/applications
```

**Request Body:**

```json
{
    "company": "Wipro",
    "role": "Python Developer",
    "status": "APPLIED"
}
```

Expected Status: `201 Created`

### 2. Get All Applications – GET

```text
GET http://127.0.0.1:5000/applications
```

Expected Status: `200 OK`

### 3. Get Application by ID – GET

```text
GET http://127.0.0.1:5000/applications/4
```

Expected Status: `200 OK`

### 4. Update Application – PUT

```text
PUT http://127.0.0.1:5000/applications/4
```

**Request Body:**

```json
{
    "status": "INTERVIEW"
}
```

Expected Status: `200 OK`

### 5. Delete Application – DELETE

```text
DELETE http://127.0.0.1:5000/applications/4
```

Expected Status: `200 OK`

## ⚠️ Error Handling

| Status Code | Description |
|---|---|
| 200 | Request successful |
| 201 | Application created successfully |
| 400 | Invalid request data |
| 404 | Application not found |
| 500 | Internal server error |

## 📅 Learning Progress

| Day | Task | Status |
|---|---|---|
| Day 1 | Flask Setup & PostgreSQL Connection | Completed |
| Day 2 | POST API & Input Validation | Completed |
| Day 3 | GET Application by ID & 404 Handling | Completed |
| Day 4 | PUT Update Application API | Completed |
| Day 5 | DELETE Application API | Completed |

## 🎯 Learning Outcomes

- Understanding Flask REST API development
- Working with PostgreSQL databases
- Performing CRUD operations
- Using SQLAlchemy ORM
- Implementing API validation and error handling
- Testing REST APIs with Postman
- Managing projects using Git and GitHub

## 👨‍💻 Author

**Prasanna**

GitHub: [Prasanna-20740](https://github.com/Prasanna-20740)

Project Repository: [Job Application Tracker](https://github.com/Prasanna-20740/Job-Application-Tracker)

---

⭐ If you find this project useful, consider giving it a star!
