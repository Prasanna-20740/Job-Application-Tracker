# 🚀 Job Application Tracker

A Job Application Tracker backend application developed using **Python, Flask, PostgreSQL, SQLAlchemy, and Docker**.

This project helps users manage job application details by creating, retrieving, and tracking applications through RESTful APIs.

## 📌 Project Overview

The Job Application Tracker is designed to manage job application records, including company name, job role, and application status.

The backend provides REST APIs to create new applications, retrieve all applications, and retrieve a specific application using its ID.

## ✨ Features

- Create new job applications.
- Retrieve all job applications.
- Retrieve a specific application by ID.
- Input validation for required fields.
- Handle application not found errors.
- Store data in PostgreSQL.
- RESTful API development using Flask.
- API testing using Postman.
- PostgreSQL database setup using Docker.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Flask | Backend Framework |
| PostgreSQL | Database |
| Flask-SQLAlchemy | ORM and Database Operations |
| Docker | Database Containerization |
| Postman | API Testing |
| Git & GitHub | Version Control |

## 📂 Project Structure

```text
Job-Application-Tracker/
│
├── app.py
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

## ⚙️ Installation & Setup

### 1. Clone Repository

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

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv
```

### 6. Start PostgreSQL Using Docker

Make sure Docker Desktop is running.

```bash
docker compose up -d
```

Verify the container:

```bash
docker ps
```

### 7. Run Flask Application

```bash
python app.py
```

Backend URL:

```text
http://127.0.0.1:5000
```

## 🔗 API Endpoints

### 1. Home API

**Method:** GET

```text
http://127.0.0.1:5000/
```

Returns the API welcome message and available endpoints.

### 2. Get All Applications

**Method:** GET

```text
http://127.0.0.1:5000/applications
```

Retrieves all job application records from PostgreSQL.

### 3. Create New Application

**Method:** POST

```text
http://127.0.0.1:5000/applications
```

**Request Body:**

```json
{
  "company": "Wipro",
  "role": "Python Developer",
  "status": "APPLIED"
}
```

**Success Response:** `201 Created`

```json
{
  "message": "Application added successfully",
  "application": {
    "id": 4,
    "company": "Wipro",
    "role": "Python Developer",
    "status": "APPLIED"
  }
}
```

### 4. Get Application by ID

**Method:** GET

```text
http://127.0.0.1:5000/applications/4
```

Retrieves a specific job application using its ID.

**Success Response:** `200 OK`

```json
{
  "id": 4,
  "company": "Wipro",
  "role": "Python Developer",
  "status": "APPLIED"
}
```

### 5. Application Not Found

If the requested application ID does not exist:

**Response:** `404 Not Found`

```json
{
  "error": "Application not found"
}
```

## 🗄️ Database Structure

**Table: JobApplication**

| Column | Data Type | Description |
|---|---|---|
| id | Integer | Primary Key |
| company | String(100) | Company Name |
| role | String(100) | Job Role |
| status | String(50) | Application Status |

## 🧪 API Testing with Postman

The following scenarios have been tested:

| Test Case | Expected Result | Status |
|---|---|---|
| Create application | 201 Created | ✅ Passed |
| Missing job role | 400 Bad Request | ✅ Passed |
| Get all applications | 200 OK | ✅ Passed |
| Get application by ID | 200 OK | ✅ Passed |
| Invalid application ID | 404 Not Found | ✅ Passed |

## 📅 Development Progress

| Day | Task | Status |
|---|---|---|
| Day 1 | Docker and PostgreSQL Setup | ✅ Completed |
| Day 1 | Flask Application Setup | ✅ Completed |
| Day 1 | SQLAlchemy Model and Database Connection | ✅ Completed |
| Day 1 | GET All Applications API | ✅ Completed |
| Day 2 | POST Application API | ✅ Completed |
| Day 2 | Input Validation | ✅ Completed |
| Day 2 | Postman API Testing | ✅ Completed |
| Day 3 | GET Application by ID API | ✅ Completed |
| Day 3 | Dynamic URL Parameters | ✅ Completed |
| Day 3 | 404 Error Handling | ✅ Completed |

## 🚀 Future Enhancements

- Update job application details using PUT API.
- Delete applications using DELETE API.
- Search applications by company name.
- Filter applications by status.
- React frontend integration.
- User authentication.
- Dashboard with application statistics.

## 👨‍💻 Developer

**Prasanna P**

Python Full Stack Developer Intern

GitHub: https://github.com/Prasanna-20740

**Project Repository:**  
https://github.com/Prasanna-20740/Job-Application-Tracker

---

⭐ Developed as part of a 60-Day Full Stack Python + React Learning Journey.
