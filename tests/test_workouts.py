from tests.conftest import signup, auth_header


def get_token(client, username="alice"):
    return signup(client, username=username).get_json()["access_token"]


def create_workout(client, token, **overrides):
    payload = {
        "exercise_name": "Running",
        "duration_minutes": 30,
        "calories_burned": 250,
        "workout_date": "2026-07-01",
        "notes": "Morning run",
    }
    payload.update(overrides)
    return client.post("/api/workouts", json=payload, headers=auth_header(token))


def test_index_requires_auth(client):
    resp = client.get("/api/workouts")
    assert resp.status_code == 401


def test_create_workout(client):
    token = get_token(client)
    resp = create_workout(client, token)
    assert resp.status_code == 201
    data = resp.get_json()["workout"]
    assert data["exercise_name"] == "Running"
    assert data["duration_minutes"] == 30


def test_create_workout_missing_required_field(client):
    token = get_token(client)
    resp = client.post(
        "/api/workouts", json={"exercise_name": "Running"}, headers=auth_header(token)
    )
    assert resp.status_code == 422


def test_index_only_returns_own_workouts(client):
    token_a = get_token(client, "alice")
    token_b = get_token(client, "bob")

    create_workout(client, token_a, exercise_name="Alice Run")
    create_workout(client, token_b, exercise_name="Bob Run")

    resp = client.get("/api/workouts", headers=auth_header(token_a))
    data = resp.get_json()
    assert data["total_items"] == 1
    assert data["workouts"][0]["exercise_name"] == "Alice Run"


def test_index_pagination(client):
    token = get_token(client)
    for i in range(5):
        create_workout(client, token, exercise_name=f"Workout {i}")

    resp = client.get("/api/workouts?page=1&per_page=2", headers=auth_header(token))
    data = resp.get_json()
    assert len(data["workouts"]) == 2
    assert data["total_items"] == 5
    assert data["total_pages"] == 3
    assert data["has_next"] is True


def test_show_own_workout(client):
    token = get_token(client)
    workout_id = create_workout(client, token).get_json()["workout"]["id"]

    resp = client.get(f"/api/workouts/{workout_id}", headers=auth_header(token))
    assert resp.status_code == 200


def test_cannot_view_other_users_workout(client):
    token_a = get_token(client, "alice")
    token_b = get_token(client, "bob")
    workout_id = create_workout(client, token_a).get_json()["workout"]["id"]

    resp = client.get(f"/api/workouts/{workout_id}", headers=auth_header(token_b))
    assert resp.status_code == 404


def test_update_own_workout(client):
    token = get_token(client)
    workout_id = create_workout(client, token).get_json()["workout"]["id"]

    resp = client.patch(
        f"/api/workouts/{workout_id}",
        json={"duration_minutes": 60},
        headers=auth_header(token),
    )
    assert resp.status_code == 200
    assert resp.get_json()["workout"]["duration_minutes"] == 60


def test_cannot_update_other_users_workout(client):
    token_a = get_token(client, "alice")
    token_b = get_token(client, "bob")
    workout_id = create_workout(client, token_a).get_json()["workout"]["id"]

    resp = client.patch(
        f"/api/workouts/{workout_id}",
        json={"duration_minutes": 60},
        headers=auth_header(token_b),
    )
    assert resp.status_code == 404


def test_delete_own_workout(client):
    token = get_token(client)
    workout_id = create_workout(client, token).get_json()["workout"]["id"]

    resp = client.delete(f"/api/workouts/{workout_id}", headers=auth_header(token))
    assert resp.status_code == 204

    resp = client.get(f"/api/workouts/{workout_id}", headers=auth_header(token))
    assert resp.status_code == 404


def test_cannot_delete_other_users_workout(client):
    token_a = get_token(client, "alice")
    token_b = get_token(client, "bob")
    workout_id = create_workout(client, token_a).get_json()["workout"]["id"]

    resp = client.delete(f"/api/workouts/{workout_id}", headers=auth_header(token_b))
    assert resp.status_code == 404
