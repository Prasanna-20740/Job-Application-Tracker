
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_jwt_extended import create_access_token

import app as app_module
from tests.factories import UserFactory, ApplicationFactory


@pytest.fixture
def app():
    app_module.app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="test-secret-key-for-pytest-at-least-32-characters",
    )

    yield app_module.app


@pytest.fixture
def db(app):
    engine = create_engine("sqlite://")
    connection = engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    test_session = scoped_session(session_factory)

    app_module.db.session = test_session

    with app.app_context():
        app_module.db.metadata.create_all(bind=connection)

        yield app_module.db

        test_session.remove()

        if transaction.is_active:
            transaction.rollback()

        connection.close()
        engine.dispose()


@pytest.fixture
def factories(db):
    UserFactory._meta.sqlalchemy_session = db.session
    ApplicationFactory._meta.sqlalchemy_session = db.session

    yield {
        "user": UserFactory,
        "application": ApplicationFactory,
    }

    UserFactory._meta.sqlalchemy_session = None
    ApplicationFactory._meta.sqlalchemy_session = None


@pytest.fixture
def auth_user(db, factories):
    user = factories["user"].create()
    db.session.flush()

    return user


@pytest.fixture
def auth_headers(app, auth_user):
    with app.app_context():
        access_token = create_access_token(
            identity=str(auth_user.id)
        )

    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture
def client(app, db, auth_headers):
    test_client = app.test_client()

    test_client.environ_base["HTTP_AUTHORIZATION"] = (
        auth_headers["Authorization"]
    )

    return test_client


@pytest.fixture
def service(db):
    return app_module.application_service
