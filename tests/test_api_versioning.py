
# ==========================================
# API VERSIONING TESTS - DAY 17
# ==========================================


# Test 1: V1 API and Deprecation Header
def test_v1_applications_returns_success_and_deprecation_header(
    client, factories, auth_user
):
    factories["application"].create(
        company="Google",
        role="Python Developer",
        user=auth_user
    )

    response = client.get("/api/v1/applications")

    assert response.status_code == 200
    assert response.json["version"] == "v1"
    assert response.headers.get("Deprecation") == "true"
    assert len(response.json["applications"]) == 1


# Test 2: V2 API Full Response
def test_v2_applications_returns_full_response(
    client, factories, auth_user
):
    factories["application"].create(
        company="Microsoft",
        role="Backend Developer",
        notes="Full response test",
        user=auth_user
    )

    response = client.get("/api/v2/applications")

    assert response.status_code == 200
    assert response.json["version"] == "v2"
    assert response.json["format"] == "full"

    application = response.json["applications"][0]

    assert application["company"] == "Microsoft"
    assert application["role"] == "Backend Developer"
    assert "notes" in application
    assert "user_id" in application
    assert "resume_path" in application


# Test 3: V2 API Summary Response
def test_v2_summary_returns_compact_response(
    client, factories, auth_user
):
    factories["application"].create(
        company="Infosys",
        role="Python Developer",
        notes="This should not appear in summary",
        user=auth_user
    )

    response = client.get(
        "/api/v2/applications?format=summary"
    )

    assert response.status_code == 200
    assert response.json["version"] == "v2"
    assert response.json["format"] == "summary"

    application = response.json["applications"][0]

    # Required summary fields
    assert application["company"] == "Infosys"
    assert application["role"] == "Python Developer"
    assert "id" in application
    assert "status" in application
    assert "applied_date" in application

    # Full response fields should be omitted
    assert "notes" not in application
    assert "user_id" not in application
    assert "resume_path" not in application


# Test 4: Invalid V2 Format
def test_v2_invalid_format_returns_400(client):
    response = client.get(
        "/api/v2/applications?format=invalid"
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Invalid format. Use full or summary"
    )


# Test 5: Authentication Required
def test_versioned_endpoints_require_authentication(app):
    unauthenticated_client = app.test_client()

    v1_response = unauthenticated_client.get(
        "/api/v1/applications"
    )

    v2_response = unauthenticated_client.get(
        "/api/v2/applications"
    )

    assert v1_response.status_code == 401
    assert v2_response.status_code == 401
