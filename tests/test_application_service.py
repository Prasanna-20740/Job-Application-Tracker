
from datetime import date

import pytest

from app import ApplicationStatus
from services.application_service import (
    ApplicationNotFound,
    DuplicateApplication,
)


# 1. Get existing application
def test_get_application(service, factories):
    created = factories["application"]()

    result = service.get_application(created.id)

    assert result.id == created.id
    assert result.company == created.company


# 2. Get application that does not exist
def test_get_application_not_found(service):
    with pytest.raises(ApplicationNotFound):
        service.get_application(9999)


# 3. Update company and role
def test_update_company_and_role(service, factories):
    application = factories["application"]()

    updated = service.update_application(
        application.id,
        {
            "company": "Microsoft",
            "role": "Backend Developer",
        },
    )

    assert updated.company == "Microsoft"
    assert updated.role == "Backend Developer"


# 4. Update status
def test_update_status(service, factories):
    application = factories["application"]()

    updated = service.update_application(
        application.id,
        {"status": "INTERVIEW"},
    )

    assert updated.status == ApplicationStatus.INTERVIEW


# 5. Update notes
def test_update_notes(service, factories):
    application = factories["application"]()

    updated = service.update_application(
        application.id,
        {"notes": "Interview scheduled"},
    )

    assert updated.notes == "Interview scheduled"


# 6. Update notes to None
def test_update_notes_to_none(service, factories):
    application = factories["application"]()

    updated = service.update_application(
        application.id,
        {"notes": None},
    )

    assert updated.notes is None


# 7. Update applied date using string
def test_update_applied_date_string(service, factories):
    application = factories["application"]()

    updated = service.update_application(
        application.id,
        {"applied_date": "2026-11-01"},
    )

    assert updated.applied_date == date(2026, 11, 1)


# 8. Update applied date using date object
def test_update_applied_date_object(service, factories):
    application = factories["application"]()

    new_date = date(2026, 10, 15)

    updated = service.update_application(
        application.id,
        {"applied_date": new_date},
    )

    assert updated.applied_date == new_date


# 9. Reject empty company
def test_update_empty_company(service, factories):
    application = factories["application"]()

    with pytest.raises(ValueError):
        service.update_application(
            application.id,
            {"company": "   "},
        )


# 10. Reject empty role
def test_update_empty_role(service, factories):
    application = factories["application"]()

    with pytest.raises(ValueError):
        service.update_application(
            application.id,
            {"role": "   "},
        )


# 11. Reject invalid company type
def test_update_invalid_company_type(service, factories):
    application = factories["application"]()

    with pytest.raises(ValueError):
        service.update_application(
            application.id,
            {"company": 123},
        )


# 12. Reject invalid status
def test_update_invalid_status(service, factories):
    application = factories["application"]()

    with pytest.raises(ValueError):
        service.update_application(
            application.id,
            {"status": "INVALID_STATUS"},
        )


# 13. Reject invalid notes
def test_update_invalid_notes(service, factories):
    application = factories["application"]()

    with pytest.raises(ValueError):
        service.update_application(
            application.id,
            {"notes": 123},
        )


# 14. Reject invalid date
def test_update_invalid_date(service, factories):
    application = factories["application"]()

    with pytest.raises(ValueError):
        service.update_application(
            application.id,
            {"applied_date": "invalid-date"},
        )


# 15. Reject duplicate application during update
def test_update_duplicate_application(service, factories):
    user = factories["user"]()

    first = service.create_application(
        company="Google",
        role="Developer",
        user_id=user.id,
    )

    second = service.create_application(
        company="Microsoft",
        role="Tester",
        user_id=user.id,
    )

    with pytest.raises(DuplicateApplication):
        service.update_application(
            second.id,
            {
                "company": "Google",
                "role": "Developer",
            },
        )


# 16. Delete application
def test_delete_application(service, db, factories):
    application = factories["application"]()
    application_id = application.id

    deleted = service.delete_application(application_id)

    assert deleted.id == application_id
    assert db.session.get(
        deleted.__class__, application_id
    ) is None


# 17. Delete missing application
def test_delete_application_not_found(service):
    with pytest.raises(ApplicationNotFound):
        service.delete_application(9999)


# 18. List applications when empty
def test_list_applications_empty(service):
    result = service.list_applications()

    assert result == []


# 19. List multiple applications
def test_list_applications(service, factories):
    factories["application"]()
    factories["application"]()

    result = service.list_applications()

    assert len(result) == 2


# 20. Reject duplicate application during creation
def test_create_duplicate_application(service):
    service.create_application(
        company="Google",
        role="Developer",
    )

    with pytest.raises(DuplicateApplication):
        service.create_application(
            company="Google",
            role="Developer",
        )
