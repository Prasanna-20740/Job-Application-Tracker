
import io
import csv
from datetime import date

from app import ApplicationStatus


def make_csv_file(content, filename="applications.csv"):
    return {
        "file": (
            io.BytesIO(content.encode("utf-8")),
            filename
        )
    }


def test_csv_export_returns_user_applications(client, factories, auth_user):
    application = factories["application"].create(
        user=auth_user,
        company="TCS",
        role="Python Developer",
        status=ApplicationStatus.APPLIED
    )

    response = client.get("/applications/export")

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "attachment" in response.headers["Content-Disposition"]

    rows = list(csv.DictReader(
        io.StringIO(response.get_data(as_text=True))
    ))

    assert len(rows) == 1
    assert rows[0]["company"] == "TCS"
    assert rows[0]["id"] == str(application.id)


def test_csv_export_does_not_include_other_users_data(
    client, factories, auth_user
):
    other_user = factories["user"].create()

    factories["application"].create(
        user=auth_user,
        company="My Company"
    )

    factories["application"].create(
        user=other_user,
        company="Other User Company"
    )

    response = client.get("/applications/export")

    csv_content = response.get_data(as_text=True)

    assert "My Company" in csv_content
    assert "Other User Company" not in csv_content


def test_csv_import_creates_new_application(client):
    csv_content = (
        "id,company,role,status,applied_date,notes\n"
        f",Infosys,React Developer,APPLIED,{date.today().isoformat()},Imported row\n"
    )

    response = client.post(
        "/applications/import",
        data=make_csv_file(csv_content),
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json["created"] == 1
    assert response.json["updated"] == 0
    assert response.json["failed"] == 0


def test_csv_import_updates_existing_application(
    client, factories, auth_user
):
    application = factories["application"].create(
        user=auth_user,
        company="TCS",
        role="Python Developer"
    )

    csv_content = (
        "id,company,role,status,applied_date,notes\n"
        f"{application.id},TCS,Python Full Stack Developer,"
        f"INTERVIEW,{date.today().isoformat()},Updated through CSV\n"
    )

    response = client.post(
        "/applications/import",
        data=make_csv_file(csv_content),
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json["updated"] == 1
    assert response.json["created"] == 0

    assert application.role == "Python Full Stack Developer"
    assert application.status == ApplicationStatus.INTERVIEW


def test_csv_import_skips_invalid_rows_and_returns_error_log(client):
    csv_content = (
        "id,company,role,status,applied_date,notes\n"
        f",Valid Company,Developer,APPLIED,{date.today().isoformat()},Valid row\n"
        f",Invalid Company,Developer,WRONG_STATUS,{date.today().isoformat()},Invalid row\n"
    )

    response = client.post(
        "/applications/import",
        data=make_csv_file(csv_content),
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "import_error_log.csv" in response.headers["Content-Disposition"]
    assert response.headers["X-Created-Count"] == "1"
    assert response.headers["X-Failed-Count"] == "1"

    error_csv = response.get_data(as_text=True)
    assert "Invalid Company" in error_csv


def test_csv_import_rejects_missing_headers(client):
    csv_content = "company,role\nTCS,Developer\n"

    response = client.post(
        "/applications/import",
        data=make_csv_file(csv_content),
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "Invalid CSV headers"


def test_bulk_status_update_updates_valid_rows(
    client, factories, auth_user
):
    first = factories["application"].create(
        user=auth_user,
        company="TCS"
    )
    second = factories["application"].create(
        user=auth_user,
        company="Infosys"
    )

    csv_content = (
        "id,status\n"
        f"{first.id},OFFER\n"
        f"{second.id},INTERVIEW\n"
    )

    response = client.post(
        "/applications/bulk-status-update",
        data=make_csv_file(csv_content, "bulk_status.csv"),
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json["updated"] == 2
    assert response.json["failed"] == 0

    assert first.status == ApplicationStatus.OFFER
    assert second.status == ApplicationStatus.INTERVIEW


def test_bulk_status_update_skips_invalid_rows(
    client, factories, auth_user
):
    application = factories["application"].create(
        user=auth_user,
        company="TCS"
    )

    csv_content = (
        "id,status\n"
        f"{application.id},REJECTED\n"
        "999999,INTERVIEW\n"
    )

    response = client.post(
        "/applications/bulk-status-update",
        data=make_csv_file(csv_content, "bulk_invalid.csv"),
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert response.headers["X-Updated-Count"] == "1"
    assert response.headers["X-Failed-Count"] == "1"

    assert application.status == ApplicationStatus.REJECTED
    assert "Application not found" in response.get_data(as_text=True)
