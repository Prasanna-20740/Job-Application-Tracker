
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import app as app_module
from tests.factories import UserFactory, ApplicationFactory


@pytest.fixture
def app():
    app_module.app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
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
def client(app, db):
    return app.test_client()


@pytest.fixture
def service(db):
    return app_module.application_service


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
