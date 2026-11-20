
from datetime import datetime

import app as app_module


def test_normal_user_cannot_delete_user(client, factories):
    target = factories["user"].create()

    response = client.delete(
        f"/admin/users/{target.id}"
    )

    assert response.status_code == 403
    assert response.json["error"] == "Admin access required"


def test_admin_can_delete_user_and_related_records(
    client,
    db,
    factories,
    admin_user,
    admin_headers
):
    # Create a test user
    target = factories["user"].create()

    # Create an application for that user
    application = factories["application"].create(
        user=target
    )

    db.session.flush()

    # Create interview
    interview = app_module.Interview(
        application_id=application.id,
        interview_date=datetime(2026, 11, 21, 10, 0)
    )

    # Create application status history
    history = app_module.ApplicationStatusHistory(
        application_id=application.id,
        status=app_module.ApplicationStatus.APPLIED
    )

    db.session.add_all([interview, history])
    db.session.flush()

    target_id = target.id
    application_id = application.id

    # Admin deletes the user
    response = client.delete(
        f"/admin/users/{target_id}",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json["deleted_applications"] == 1

    # Verify user deletion
    assert db.session.get(
        app_module.User, target_id
    ) is None

    # Verify application deletion
    assert db.session.get(
        app_module.JobApplication, application_id
    ) is None

    # Verify interview deletion
    assert app_module.Interview.query.filter_by(
        application_id=application_id
    ).count() == 0

    # Verify status history deletion
    assert app_module.ApplicationStatusHistory.query.filter_by(
        application_id=application_id
    ).count() == 0

    # Verify audit log
    audit = app_module.AuditLog.query.filter_by(
        action="DELETE_USER",
        target_user_id=target_id
    ).first()

    assert audit is not None
    assert audit.actor_user_id == admin_user.id
    assert audit.target_username is not None
    assert audit.details["deleted_applications"] == 1


def test_admin_cannot_delete_own_account(
    client,
    admin_user,
    admin_headers
):
    response = client.delete(
        f"/admin/users/{admin_user.id}",
        headers=admin_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "You cannot delete your own account"
    )


def test_admin_delete_user_not_found(
    client,
    admin_headers
):
    response = client.delete(
        "/admin/users/999999",
        headers=admin_headers
    )

    assert response.status_code == 404
    assert response.json["error"] == "User not found"


def test_admin_can_impersonate_user(
    client,
    db,
    factories,
    admin_user,
    admin_headers
):
    from flask_jwt_extended import decode_token

    target = factories["user"].create()
    db.session.flush()

    response = client.post(
        f"/admin/users/{target.id}/impersonate",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json["is_impersonation"] is True

    token = response.json["access_token"]

    with client.application.app_context():
        decoded = decode_token(token)

    assert decoded["sub"] == str(target.id)
    assert decoded["is_impersonation"] is True
    assert decoded["impersonated_by"] == admin_user.id

    audit = app_module.AuditLog.query.filter_by(
        action="IMPERSONATE_USER",
        target_user_id=target.id
    ).first()

    assert audit is not None
    assert audit.actor_user_id == admin_user.id


def test_normal_user_cannot_impersonate(
    client,
    factories
):
    target = factories["user"].create()

    response = client.post(
        f"/admin/users/{target.id}/impersonate"
    )

    assert response.status_code == 403


def test_admin_cannot_impersonate_another_admin(
    client,
    db,
    factories,
    admin_headers
):
    another_admin = factories["user"].create(
        role=app_module.Role.ADMIN
    )
    db.session.flush()

    response = client.post(
        f"/admin/users/{another_admin.id}/impersonate",
        headers=admin_headers
    )

    assert response.status_code == 403
    assert response.json["error"] == (
        "Cannot impersonate another admin"
    )
