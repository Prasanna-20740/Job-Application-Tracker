
from datetime import date

import pytest
import app as app_module


# ---------------------------------
# is_valid_user_id tests
# ---------------------------------

def test_valid_user_id_none(app):
    assert app_module.is_valid_user_id(None) is True


def test_valid_user_id_existing(app, factories):
    user = factories["user"].create()

    assert app_module.is_valid_user_id(user.id) is True


def test_valid_user_id_non_existing(app, db):
    assert app_module.is_valid_user_id(9999) is False


def test_valid_user_id_string(app):
    assert app_module.is_valid_user_id("1") is False


def test_valid_user_id_boolean(app):
    assert app_module.is_valid_user_id(True) is False


# ---------------------------------
# parse_application_data tests
# ---------------------------------

def test_parse_application_data_success():
    result = app_module.parse_application_data({
        "company": " Google ",
        "role": " Python Developer ",
        "notes": " Test notes ",
        "status": "interview",
        "applied_date": "2026-11-11"
    }, creating=True)

    assert result["company"] == "Google"
    assert result["role"] == "Python Developer"
    assert result["notes"] == "Test notes"
    assert result["status"] == "INTERVIEW"
    assert result["applied_date"] == date(2026, 11, 11)


def test_parse_application_data_not_dict():
    with pytest.raises(ValueError):
        app_module.parse_application_data("invalid")


def test_parse_missing_company():
    with pytest.raises(ValueError, match="Company is required"):
        app_module.parse_application_data(
            {"role": "Developer"},
            creating=True
        )


def test_parse_missing_role():
    with pytest.raises(ValueError, match="Role is required"):
        app_module.parse_application_data(
            {"company": "Google"},
            creating=True
        )


@pytest.mark.parametrize("company", ["", "   ", 123, None])
def test_parse_invalid_company(company):
    with pytest.raises(ValueError):
        app_module.parse_application_data({"company": company})


@pytest.mark.parametrize("role", ["", "   ", 123, None])
def test_parse_invalid_role(role):
    with pytest.raises(ValueError):
        app_module.parse_application_data({"role": role})


def test_parse_invalid_notes():
    with pytest.raises(ValueError, match="Notes must be a string or null"):
        app_module.parse_application_data({"notes": 123})


def test_parse_none_notes():
    result = app_module.parse_application_data({"notes": None})

    assert result["notes"] is None


def test_parse_invalid_status_type():
    with pytest.raises(ValueError, match="Status must be a string"):
        app_module.parse_application_data({"status": 123})


def test_parse_invalid_status_value():
    with pytest.raises(ValueError, match="Invalid status"):
        app_module.parse_application_data({"status": "UNKNOWN"})


def test_parse_invalid_date_type():
    with pytest.raises(ValueError):
        app_module.parse_application_data({
            "applied_date": date.today()
        })


def test_parse_invalid_date_value():
    with pytest.raises(ValueError, match="Invalid applied_date"):
        app_module.parse_application_data({
            "applied_date": "invalid-date"
        })


def test_parse_invalid_user_id(app, db):
    with pytest.raises(ValueError, match="Invalid user_id"):
        app_module.parse_application_data({"user_id": 9999})


def test_parse_valid_user_id(app, factories):
    user = factories["user"].create()

    result = app_module.parse_application_data({
        "user_id": user.id
    })

    assert result["user_id"] == user.id


# ---------------------------------
# delete_resume_file tests
# ---------------------------------

def test_delete_resume_file_success(app, tmp_path):
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    resume = tmp_path / "resume.pdf"
    resume.write_bytes(b"test pdf")

    app_module.delete_resume_file("uploads/resume.pdf")

    assert not resume.exists()


def test_delete_resume_file_none():
    app_module.delete_resume_file(None)


def test_delete_resume_file_empty():
    app_module.delete_resume_file("")


def test_delete_resume_file_not_found(app, tmp_path):
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    app_module.delete_resume_file("uploads/missing.pdf")


def test_delete_resume_file_os_error(app, tmp_path, monkeypatch):
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    resume = tmp_path / "resume.pdf"
    resume.write_bytes(b"test pdf")

    def raise_os_error(path):
        raise OSError("Permission denied")

    monkeypatch.setattr(app_module.os, "remove", raise_os_error)

    app_module.delete_resume_file("uploads/resume.pdf")

    assert resume.exists()

# extract_pdf_text tests

class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    is_encrypted = False

    def __init__(self):
        self.pages = [
            FakePage("Python Developer"),
            FakePage(None),
            FakePage("Flask and PostgreSQL"),
        ]


def test_extract_pdf_text_success(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "PdfReader",
        lambda file_path: FakeReader()
    )

    result = app_module.extract_pdf_text("dummy.pdf")

    assert result == "Python Developer\nFlask and PostgreSQL"


def test_extract_pdf_text_encrypted(monkeypatch):
    class EncryptedReader:
        is_encrypted = True

    monkeypatch.setattr(
        app_module,
        "PdfReader",
        lambda file_path: EncryptedReader()
    )

    with pytest.raises(ValueError):
        app_module.extract_pdf_text("encrypted.pdf")


def test_extract_pdf_text_empty(monkeypatch):
    class EmptyReader:
        is_encrypted = False
        pages = []

    monkeypatch.setattr(
        app_module,
        "PdfReader",
        lambda file_path: EmptyReader()
    )

    result = app_module.extract_pdf_text("empty.pdf")

    assert result == ""

