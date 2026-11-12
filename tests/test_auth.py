
def register_user(client, username="authuser", email="authuser@example.com"):
    return client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345"
        }
    )


def login_user(client, email="authuser@example.com"):
    return client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "Test@12345"
        }
    )


def test_register_success(client):
    response = register_user(client)

    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"
    assert response.json["user"]["username"] == "authuser"
    assert "password_hash" not in response.json["user"]


def test_register_missing_fields(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser"}
    )

    assert response.status_code == 400


def test_register_short_password(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "Password must be at least 8 characters"


def test_register_duplicate_user(client):
    register_user(client)

    response = register_user(client)

    assert response.status_code == 409


def test_login_success(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200
    assert response.json["message"] == "Login successful"
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_invalid_password(client):
    register_user(client)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "authuser@example.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401
    assert response.json["error"] == "Invalid email or password"


def test_refresh_token_success(client):
    register_user(client)

    login_response = login_user(client)

    refresh_token = login_response.json["refresh_token"]

    response = client.post(
        "/api/auth/refresh",
        headers={
            "Authorization": f"Bearer {refresh_token}"
        }
    )

    assert response.status_code == 200
    assert response.json["message"] == "Access token refreshed successfully"
    assert "access_token" in response.json


def test_logout_revokes_access_and_refresh_tokens(client):
    register_user(client)

    login_response = login_user(client)

    access_token = login_response.json["access_token"]
    refresh_token = login_response.json["refresh_token"]

    logout_response = client.post(
        "/api/auth/logout",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "refresh_token": refresh_token
        }
    )

    assert logout_response.status_code == 200

    # Access token should be rejected
    access_response = client.get(
        "/applications",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert access_response.status_code == 401

    # Refresh token should also be rejected
    refresh_response = client.post(
        "/api/auth/refresh",
        headers={
            "Authorization": f"Bearer {refresh_token}"
        }
    )

    assert refresh_response.status_code == 401


def test_protected_endpoint_without_token(app):
    unauthenticated_client = app.test_client()

    response = unauthenticated_client.get("/applications")

    assert response.status_code == 401
