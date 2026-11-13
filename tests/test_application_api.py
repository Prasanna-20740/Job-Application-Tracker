
def test_home_api(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Job Application Tracker API is running"


def test_create_user(client):
    response = client.post("/users", json={
        "username": "prasanna",
        "email": "prasanna@example.com"
    })

    assert response.status_code == 201
    assert response.json["user"]["username"] == "prasanna"


def test_create_user_missing_username(client):
    response = client.post("/users", json={
        "email": "test@example.com"
    })

    assert response.status_code == 400
    assert response.json["error"] == "Username is required"


def test_create_user_missing_email(client):
    response = client.post("/users", json={
        "username": "testuser"
    })

    assert response.status_code == 400
    assert response.json["error"] == "Email is required"


def test_create_duplicate_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    client.post("/users", json=user_data)
    response = client.post("/users", json=user_data)

    assert response.status_code == 409


def test_get_users(client):
    client.post("/users", json={
        "username": "user1",
        "email": "user1@example.com"
    })

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json) == 2

    usernames = [
        user["username"]
        for user in response.json
    ]

    assert "user1" in usernames


def test_create_application(client):
    response = client.post("/applications", json={
        "company": "Google",
        "role": "Python Developer",
        "status": "APPLIED",
        "notes": "Testing application"
    })

    assert response.status_code == 201
    assert response.json["application"]["company"] == "Google"


def test_create_application_missing_company(client):
    response = client.post("/applications", json={
        "role": "Python Developer"
    })

    assert response.status_code == 422


def test_create_application_missing_role(client):
    response = client.post("/applications", json={
        "company": "Google"
    })

    assert response.status_code == 422


def test_get_applications(client):
    client.post("/applications", json={
        "company": "Google",
        "role": "Developer"
    })

    response = client.get("/applications")

    assert response.status_code == 200
    assert len(response.json["applications"]) == 1
    assert response.json["applications"][0]["company"] == "Google"


def test_get_application_by_id(client):
    create_response = client.post("/applications", json={
        "company": "Google",
        "role": "Developer"
    })

    application_id = create_response.json["application"]["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json["company"] == "Google"


def test_get_application_not_found(client):
    response = client.get("/applications/9999")

    assert response.status_code == 404


def test_update_application(client):
    create_response = client.post("/applications", json={
        "company": "Google",
        "role": "Developer"
    })

    application_id = create_response.json["application"]["id"]

    response = client.patch(
        f"/applications/{application_id}",
        json={"company": "Microsoft"}
    )

    assert response.status_code == 200
    assert response.json["application"]["company"] == "Microsoft"


def test_update_application_empty_data(client):
    create_response = client.post("/applications", json={
        "company": "Google",
        "role": "Developer"
    })

    application_id = create_response.json["application"]["id"]

    response = client.patch(
        f"/applications/{application_id}",
        json={}
    )

    assert response.status_code == 400


def test_update_application_not_found(client):
    response = client.patch(
        "/applications/9999",
        json={"company": "Microsoft"}
    )

    assert response.status_code == 404


def test_delete_application(client):
    create_response = client.post("/applications", json={
        "company": "Google",
        "role": "Developer"
    })

    application_id = create_response.json["application"]["id"]

    response = client.delete(f"/applications/{application_id}")

    assert response.status_code == 200

    get_response = client.get(f"/applications/{application_id}")
    assert get_response.status_code == 404


def test_delete_application_not_found(client):
    response = client.delete("/applications/9999")

    assert response.status_code == 404
