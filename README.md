# 🚀 Job Application Tracker

A Python-based Job Application Tracker built using **Flask, PostgreSQL, SQLAlchemy, and Docker**. This project helps users organize and manage job application records, including company names, job roles, and application statuses.

## 📌 Project Overview

The Job Application Tracker is designed to simplify the process of tracking job applications in one place. It uses a Flask backend and PostgreSQL database to store application details reliably.

## 🛠️ Technologies Used

- **Python** – Backend programming
- **Flask** – Web application framework
- **Flask-SQLAlchemy** – Database ORM
- **PostgreSQL** – Relational database
- **Docker** – Database containerization
- **Docker Compose** – Container management
- **HTML, CSS, JavaScript** – Frontend technologies (planned/integrated as applicable)

## ✨ Key Features

- Store job application details.
- Manage company names and job roles.
- Track application statuses.
- PostgreSQL database integration.
- Docker-based database setup.
- SQLAlchemy database models.
- Modular project structure.

## 📂 Project Structure

```text
Job-Application-Tracker/
│
├── api/
│   └── __init__.py
│
├── models/
│   └── __init__.py
│
├── services/
│   └── __init__.py
│
├── tests/
│
├── .env
├── app.py
├── seed.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Job-Application-Tracker
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start PostgreSQL Using Docker

```bash
docker compose up -d
```

### 6. Configure Database

Configure your PostgreSQL database connection using environment variables in your `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/job_tracker
```

Keep your actual credentials private. Ensure `app.py` is configured to load this environment variable.

### 7. Run the Application

```bash
python app.py
```

## 🗄️ Database Details

**Database:** PostgreSQL

**Database Name:** `job_tracker`

**Table:** JobApplication

| Column | Description |
|---|---|
| id | Unique application ID |
| company | Company name |
| role | Job position |
| status | Application status |

## 🎯 Project Goals

- Improve Python backend development skills.
- Understand Flask application architecture.
- Gain practical experience with PostgreSQL.
- Learn Docker and container management.
- Build a real-world database-driven application.

## 🚀 Future Enhancements

- User authentication and authorization.
- Add, edit, delete, and search applications.
- Application status dashboard.
- Interview scheduling and reminders.
- Analytics and application statistics.
- Responsive frontend dashboard.

## 👨‍💻 Developer

**Prasanna P**

Python Developer | Full Stack Developer

GitHub: https://github.com/Prasanna-20740

---

⭐ If you find this project useful, consider giving it a star!
