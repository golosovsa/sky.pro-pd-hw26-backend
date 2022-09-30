import pytest

from app.config import TestingConfig
from app.server import create_app
from app.setup.db import db as database


@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture()
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()

    yield database

    database.session.close()


@pytest.fixture()
def client(app, db):
    with app.test_client() as client:
        yield client
