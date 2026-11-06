# Job Application Tracker 🚀

A backend-focused Job Application Tracker built using **Python Flask, PostgreSQL, SQLAlchemy, and Docker**. This project helps manage job application details through RESTful APIs.

## 📌 Project Overview

The Job Application Tracker is designed to store and retrieve job application details such as company name, job role, and application status.

The backend provides REST APIs to create new job applications, validate user input, and retrieve saved application records from a PostgreSQL database.

## ✨ Features

- Create new job applications using POST API.
- Retrieve all job applications using GET API.
- Store application details in PostgreSQL.
- Input validation for required fields.
- JSON-based API responses.
- Database management using SQLAlchemy.
- PostgreSQL container setup using Docker.
- API testing using Postman.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Backend framework |
| Flask-SQLAlchemy | Database ORM |
| PostgreSQL | Relational database |
| Docker | Database containerization |
| Postman | API testing |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
Job-Application-Tracker/
│
├── .venv/
├── app.py
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

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

**Windows:**

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

Check the running container:

```bash
docker ps
```

### 7. Run Flask Application

```bash
python app.py
```

Backend server:

```text
http://127.0.0.1:5000
```

## 🔗 API Endpoints

### 1. Get All Applications

**Endpoint:** `GET /applications`

```text
http://127.0.0.1:5000/applications
```

Returns all job application records stored in PostgreSQL.

### 2. Create New Application

**Endpoint:** `POST /applications`

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

**Successful Response:** `201 Created`

```json
{
  "application": {
    "id": 1,
    "company": "Wipro",
    "role": "Python Developer",
    "status": "APPLIED"
  },
  "message": "Application added successfully"
}
```

### 3. Input Validation

If the required job role is missing, the API returns:

**Response:** `400 Bad Request`

```json
{
  "error": "Job role is required"
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

The APIs are tested using Postman.

Tested scenarios:

- POST request with valid application details – `201 Created`.
- POST request without job role – `400 Bad Request`.
- GET request to retrieve all applications – `200 OK`.
- Verified saved records through the GET API.

## 📅 Development Progress

| Day | Task | Status |
|---|---|---|
| Day 1 | Docker, PostgreSQL and Flask setup | ✅ Completed |
| Day 1 | SQLAlchemy model and database connection | ✅ Completed |
| Day 1 | GET All Applications API | ✅ Completed |
| Day 2 | POST Application API | ✅ Completed |
| Day 2 | Input Validation | ✅ Completed |
| Day 2 | Postman API Testing | ✅ Completed |

## 🚀 Future Enhancements

- Get application by ID.
- Update job application details.
- Delete job applications.
- Search and filter applications.
- React frontend integration.
- Dashboard with application statistics.
- User authentication and authorization.

## 👨‍💻 Developer

**Prasanna P**

Aspiring Python Full Stack Developer

- GitHub: https://github.com/Prasanna-20740

---

⭐ If you find this project interesting, feel free to explore the repository!

**Built as part of a 60-Day Full Stack Python + React Learning Journey.**
