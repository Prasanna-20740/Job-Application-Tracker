
from datetime import date

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import User, JobApplication, ApplicationStatus


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    username = factory.Sequence(
        lambda n: f"user{n}"
    )

    email = factory.Sequence(
        lambda n: f"user{n}@example.com"
    )


class ApplicationFactory(SQLAlchemyModelFactory):

    class Meta:
        model = JobApplication
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    company = factory.Sequence(
        lambda n: f"Company {n}"
    )

    role = factory.Sequence(
        lambda n: f"Developer {n}"
    )

    status = ApplicationStatus.APPLIED

    applied_date = factory.LazyFunction(date.today)

    notes = "Test application"

    user = factory.SubFactory(UserFactory)
