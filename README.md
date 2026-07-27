# Workout Log API

A secure Flask REST API with JWT authentication and a user-owned **Workout Log** resource. Built for the Full Auth Flask Backend summative lab. Users can sign up, log in, and manage a private log of their own workouts — full CRUD with pagination — with no ability to see or touch another user's records.

## Project structure

```
workout-tracker-api/
├── app/
│   ├── __init__.py         # app factory
│   ├── extensions.py       # db, migrate, bcrypt, jwt instances
│   ├── models/
│   │   ├── user.py         # User model (bcrypt password, unique username)
│   │   └── workout.py      # WorkoutLog model (owned by User)
│   ├── schemas/
│   │   ├── user_schema.py      # signup/login validation
│   │   └── workout_schema.py   # workout create/update validation
│   └── routes/
│       ├── auth.py         # /api/auth/* endpoints
│       └── workouts.py     # /api/workouts/* endpoints
├── migrations/              # Flask-Migrate/Alembic migrations
├── tests/                    # pytest suite (auth + workouts + ownership)
├── config.py
├── run.py                    # flask entry point / shell context
├── seed.py                   # Faker-based database seeding
├── Pipfile
├── requirements.txt
└── .flaskenv
```

## Installation

Using **pipenv**:

```bash
pipenv install
pipenv shell
```

Or using **pip** + venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then set up the database:

```bash
export FLASK_APP=run.py        # already set via .flaskenv if using pipenv/flask CLI
flask db init                  # only needed if migrations/ folder is missing
flask db upgrade
python seed.py                 # optional: creates demo data
```

The seed script creates a demo account:
- **username:** `demo`
- **password:** `password123`

## Running the app

```bash
flask run
```

The API runs on `http://127.0.0.1:5000` by default.

## Running tests

```bash
python -m pytest tests/ -v
```

19 tests cover signup/login validation, password hashing, `/me`, workout CRUD, pagination, and cross-user ownership protection.

## Authentication

This API uses **JWT** (via `flask-jwt-extended`). After signup or login, the response includes an `access_token`. Send it on every protected request:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Auth — `/api/auth`

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| POST | `/api/auth/signup` | No | Create a new user. Body: `{ "username", "password" }`. Returns user + access token. Rejects duplicate usernames (422). |
| POST | `/api/auth/login` | No | Log in with username/password. Returns user + access token, or 401 on bad credentials. |
| GET | `/api/auth/me` | Yes | Returns the currently authenticated user (based on the JWT). 401 if token missing/invalid/expired. |

### Workout Logs — `/api/workouts`

All routes below require a valid JWT and only ever operate on the logged-in user's own workouts. Requesting or modifying another user's workout returns `404` (not `403`), so existence of other users' records is never leaked.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/workouts?page=1&per_page=10` | Paginated list of the current user's workouts, newest first. Returns `page`, `per_page`, `total_pages`, `total_items`, `has_next`, `has_prev`. |
| POST | `/api/workouts` | Create a workout. Body: `exercise_name` (str, required), `duration_minutes` (int, required), `calories_burned` (int, optional), `workout_date` (YYYY-MM-DD, optional, defaults to today), `notes` (str, optional). |
| GET | `/api/workouts/<id>` | Fetch a single workout owned by the current user. |
| PATCH / PUT | `/api/workouts/<id>` | Partially update a workout owned by the current user. Any subset of the fields above. |
| DELETE | `/api/workouts/<id>` | Delete a workout owned by the current user. Returns `204`. |

### Misc

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Basic health check, returns `{ "status": "ok" }`. |

## Data model

**User**
- `id`, `username` (unique), `password_hash` (bcrypt, never exposed), `created_at`

**WorkoutLog** (belongs to a User)
- `id`, `user_id` (FK), `exercise_name`, `duration_minutes`, `calories_burned`, `workout_date`, `notes`, `created_at`, `updated_at`

## Notes on design decisions

- Ownership checks are centralized in a single helper (`_get_owned_workout_or_error`) in `app/routes/workouts.py` so every show/update/delete route enforces the same rule the same way.
- Marshmallow schemas validate all incoming payloads before they touch the database, returning `422` with field-level error messages on bad input.
- Passwords are only ever stored as bcrypt hashes via a property setter on `User`; there is no way to read the hash back out.
