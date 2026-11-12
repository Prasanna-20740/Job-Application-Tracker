import pytest
import app as app_module
import io
import os
from unittest.mock import patch


def create_application(client):
    response = client.post("/applications", json={
        "company": "Google",
        "role": "Python Developer"
    })

    assert response.status_code == 201
    return response.json["application"]["id"]


def test_upload_resume_success(client, app):
    application_id = create_application(client)

    response = client.post(
        f"/applications/{application_id}/resume",
        data={
            "resume": (
                io.BytesIO(b"%PDF-1.4 test pdf content"),
                "resume.pdf"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 201
    assert response.json["message"] == "Resume uploaded successfully"

    resume_path = response.json["resume_path"]
    filename = os.path.basename(resume_path)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    assert os.path.isfile(file_path)

    os.remove(file_path)


def test_upload_resume_missing_file(client):
    application_id = create_application(client)

    response = client.post(
        f"/applications/{application_id}/resume",
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "Resume file is required"


def test_upload_resume_empty_filename(client):
    application_id = create_application(client)

    response = client.post(
        f"/applications/{application_id}/resume",
        data={
            "resume": (io.BytesIO(b"%PDF-test"), "")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "No file selected"


def test_upload_resume_invalid_extension(client):
    application_id = create_application(client)

    response = client.post(
        f"/applications/{application_id}/resume",
        data={
            "resume": (
                io.BytesIO(b"%PDF-test"),
                "resume.txt"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "Only PDF files are allowed"


def test_upload_resume_invalid_pdf_signature(client):
    application_id = create_application(client)

    response = client.post(
        f"/applications/{application_id}/resume",
        data={
            "resume": (
                io.BytesIO(b"This is not a PDF"),
                "resume.pdf"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "Invalid PDF file"


def test_upload_resume_application_not_found(client):
    response = client.post(
        "/applications/9999/resume",
        data={
            "resume": (
                io.BytesIO(b"%PDF-test"),
                "resume.pdf"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 404


def test_extract_skills():
    from app import extract_skills

    skills = extract_skills(
        "Python Flask Django PostgreSQL Docker React"
    )

    assert "Python" in skills
    assert "Flask" in skills
    assert "Django" in skills
    assert "PostgreSQL" in skills
    assert "Docker" in skills
    assert "React" in skills


def test_extract_skills_case_insensitive():
    from app import extract_skills

    skills = extract_skills("python flask JAVASCRIPT")

    assert "Python" in skills
    assert "Flask" in skills
    assert "JavaScript" in skills


def test_extract_skills_no_match():
    from app import extract_skills

    skills = extract_skills("I know communication and teamwork")

    assert skills == []


def test_resume_skills_without_upload(client):
    application_id = create_application(client)

    response = client.get(
        f"/applications/{application_id}/resume/skills"
    )

    assert response.status_code == 404
    assert "No resume uploaded" in response.json["error"]


def test_resume_skills_application_not_found(client):
    response = client.get(
        "/applications/9999/resume/skills"
    )

    assert response.status_code == 404


def test_serve_resume_not_found(client):
    response = client.get("/files/uploads/nonexistent.pdf")

    assert response.status_code == 404


def test_get_resume_skills_success(
    app, client, db, factories, auth_user, tmp_path, monkeypatch
):
    # Temporary upload folder
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    # Create a dummy resume file
    resume_file = tmp_path / "resume.pdf"
    resume_file.write_bytes(b"dummy pdf content")

    # Create application for authenticated user
    application = factories["application"].create(
        user=auth_user
    )

    application.resume_path = "uploads/resume.pdf"
    db.session.commit()

    # Mock PDF text extraction
    monkeypatch.setattr(
        app_module,
        "extract_pdf_text",
        lambda file_path: "Python Flask PostgreSQL"
    )

    response = client.get(
        f"/applications/{application.id}/resume/skills"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["application_id"] == application.id
    assert data["extracted_text"] == "Python Flask PostgreSQL"
    assert "Python" in data["skills"]
    assert "Flask" in data["skills"]