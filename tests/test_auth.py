from tests.conftest import signup, auth_header


def test_signup_creates_user(client):
    resp = signup(client)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["user"]["username"] == "alice"
    assert "access_token" in data


def test_signup_duplicate_username_fails(client):
    signup(client)
    resp = signup(client)
    assert resp.status_code == 422


def test_signup_requires_username_and_password(client):
    resp = client.post("/api/auth/signup", json={"username": "bob"})
    assert resp.status_code == 422


def test_login_with_correct_credentials(client):
    signup(client)
    resp = client.post(
        "/api/auth/login", json={"username": "alice", "password": "password123"}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()


def test_login_with_wrong_password_fails(client):
    signup(client)
    resp = client.post(
        "/api/auth/login", json={"username": "alice", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_me_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_returns_current_user(client):
    token = signup(client).get_json()["access_token"]
    resp = client.get("/api/auth/me", headers=auth_header(token))
    assert resp.status_code == 200
    assert resp.get_json()["user"]["username"] == "alice"


def test_password_is_not_stored_in_plaintext(app):
    from app.models import User

    with app.app_context():
        user = User(username="carol")
        user.password_hash = "supersecret"
        assert user._password_hash != "supersecret"
        assert user.authenticate("supersecret") is True
        assert user.authenticate("wrong") is False
