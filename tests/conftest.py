import pytest

from app import create_app
from app.extensions import db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret"


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def signup(client, username="alice", password="password123"):
    return client.post(
        "/api/auth/signup", json={"username": username, "password": password}
    )


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}
