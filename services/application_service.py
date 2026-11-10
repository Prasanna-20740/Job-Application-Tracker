
from datetime import date
import logging

# Logger setup
logger = logging.getLogger(__name__)


# Custom Exceptions
class ApplicationNotFound(Exception):
    """Raised when an application does not exist."""
    pass


class DuplicateApplication(Exception):
    """Raised when a duplicate application is created."""
    pass


# Application Service
class ApplicationService:

    def __init__(self, db, JobApplication, ApplicationStatus):
        self.db = db
        self.JobApplication = JobApplication
        self.ApplicationStatus = ApplicationStatus

    # 1. Create Application
    def create_application(
        self,
        company,
        role,
        status="APPLIED",
        notes=None,
        applied_date=None,
        user_id=None
    ):
        try:
            company = company.strip()
            role = role.strip()

            # Check duplicate application
            existing = self.JobApplication.query.filter_by(
                company=company,
                role=role,
                user_id=user_id
            ).first()

            if existing:
                raise DuplicateApplication(
                    "This application already exists"
                )

            # Validate status
            if isinstance(status, str):
                application_status = self.ApplicationStatus(
                    status.strip().upper()
                )
            else:
                application_status = status

            # Create application
            application = self.JobApplication(
                company=company,
                role=role,
                status=application_status,
                notes=notes,
                applied_date=applied_date or date.today(),
                user_id=user_id
            )

            self.db.session.add(application)
            self.db.session.commit()

            logger.info(
                "Application created successfully: ID %s",
                application.id
            )

            return application

        except DuplicateApplication:
            self.db.session.rollback()
            logger.warning("Duplicate application detected")
            raise

        except Exception:
            self.db.session.rollback()
            logger.exception("Failed to create application")
            raise

    # 2. Get Application by ID
    def get_application(self, application_id):
        application = self.db.session.get(
            self.JobApplication,
            application_id
        )

        if application is None:
            logger.warning(
                "Application not found: ID %s",
                application_id
            )
            raise ApplicationNotFound(
                "Application not found"
            )

        logger.info(
            "Application retrieved: ID %s",
            application_id
        )

        return application

    # 3. Update Application
    def update_application(self, application_id, data):
        try:
            application = self.get_application(application_id)

            new_company = data.get(
                "company", application.company
            )
            new_role = data.get(
                "role", application.role
            )
            new_user_id = data.get(
                "user_id", application.user_id
            )

            # Validate company
            if not isinstance(new_company, str) or not new_company.strip():
                raise ValueError("Valid company name is required")

            # Validate role
            if not isinstance(new_role, str) or not new_role.strip():
                raise ValueError("Valid job role is required")

            # Check duplicate excluding current application
            duplicate = self.JobApplication.query.filter(
                self.JobApplication.company == new_company.strip(),
                self.JobApplication.role == new_role.strip(),
                self.JobApplication.user_id == new_user_id,
                self.JobApplication.id != application_id
            ).first()

            if duplicate:
                raise DuplicateApplication(
                    "This application already exists"
                )

            application.company = new_company.strip()
            application.role = new_role.strip()

            # Update status
            if "status" in data:
                status = data["status"]

                if not isinstance(status, str):
                    raise ValueError("Valid status is required")

                application.status = self.ApplicationStatus(
                    status.strip().upper()
                )

            # Update notes
            if "notes" in data:
                notes = data["notes"]

                if notes is not None and not isinstance(notes, str):
                    raise ValueError("Notes must be a string")

                application.notes = notes

            # Update applied date
            if "applied_date" in data:
                applied_date = data["applied_date"]

                if isinstance(applied_date, str):
                    applied_date = date.fromisoformat(applied_date)

                if not isinstance(applied_date, date):
                    raise ValueError("Invalid applied date")

                application.applied_date = applied_date

            # Update user ID
            if "user_id" in data:
                application.user_id = new_user_id

            self.db.session.commit()

            logger.info(
                "Application updated: ID %s",
                application_id
            )

            return application

        except (ApplicationNotFound, DuplicateApplication, ValueError):
            self.db.session.rollback()
            raise

        except Exception:
            self.db.session.rollback()
            logger.exception("Failed to update application")
            raise

    # 4. Delete Application
    def delete_application(self, application_id):
        try:
            application = self.get_application(application_id)

            self.db.session.delete(application)
            self.db.session.commit()

            logger.info(
                "Application deleted: ID %s",
                application_id
            )

            return application

        except ApplicationNotFound:
            self.db.session.rollback()
            raise

        except Exception:
            self.db.session.rollback()
            logger.exception("Failed to delete application")
            raise

    # 5. List All Applications
    def list_applications(self):
        try:
            applications = self.JobApplication.query.order_by(
                self.JobApplication.id
            ).all()

            logger.info(
                "Retrieved %s applications",
                len(applications)
            )

            return applications

        except Exception:
            logger.exception("Failed to list applications")
            raise
