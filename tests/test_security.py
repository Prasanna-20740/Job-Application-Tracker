from services.security_service import sanitize_notes


def test_sanitize_normal_text():
    result = sanitize_notes("Normal application notes")

    assert result == "Normal application notes"


def test_sanitize_html_tags():
    result = sanitize_notes("<b>Important</b>")

    assert result == "Important"


def test_sanitize_script_tag():
    result = sanitize_notes("<script>alert(1)</script>")

    assert result == ""


def test_sanitize_malicious_image_tag():
    result = sanitize_notes(
        "<img src=x onerror=alert(1)>"
    )

    assert result == ""


def test_sanitize_none():
    result = sanitize_notes(None)

    assert result is None


def test_sanitize_whitespace():
    result = sanitize_notes("  Important notes  ")

    assert result == "Important notes"

from app import app


def test_security_headers():
    client = app.test_client()
    response = client.get("/")

    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert (
        response.headers.get("Referrer-Policy")
        == "strict-origin-when-cross-origin"
    )


def test_cors_allows_react_frontend():
    client = app.test_client()

    response = client.get(
        "/",
        headers={"Origin": "http://localhost:3000"}
    )

    assert (
        response.headers.get("Access-Control-Allow-Origin")
        == "http://localhost:3000"
    )


def test_cors_blocks_unapproved_origin():
    client = app.test_client()

    response = client.get(
        "/",
        headers={"Origin": "http://localhost:3001"}
    )

    assert response.headers.get("Access-Control-Allow-Origin") is None