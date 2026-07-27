# Workout Tracker API

A Flask REST API that allows users to create accounts and manage their personal workout records.

Users can register, log in securely, and create, view, update, and delete their own workouts. The API uses JWT authentication to protect user data.

## Features

- User registration and login
- JWT authentication
- Secure password hashing
- Workout CRUD operations
- User-specific workout access
- Pagination support
- Database migrations
- Automated testing with pytest


## Project Structure

```
workout-tracker-api/

├── app/
│   ├── models/
│   │   ├── user.py
│   │   └── workout.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   └── workouts.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── workout_schema.py
│   │
│   ├── extensions.py
│   └── __init__.py
│
├── migrations/
├── tests/
├── config.py
├── run.py
├── seed.py
├── requirements.txt
├── Pipfile
└── .flaskenv
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Run migrations:

```bash
flask db upgrade
```

To create sample data:

```bash
python seed.py
```

Demo account:

```
Username: demo
Password: password123
```

## Running the Application

Start the Flask server:

```bash
flask run
```

The API will run at:

```
http://127.0.0.1:5000
```


## Running Tests

Run the tests using:

```bash
pytest
```

The project includes tests for:

- User signup
- User login
- Authentication
- Creating workouts
- Viewing workouts
- Updating workouts
- Deleting workouts
- User ownership protection


# API Documentation

## Authentication Routes

### Register User

```
POST /api/auth/signup
```

Example request:

```json
{
    "username": "stephen",
    "password": "password123"
}
```

---

### Login User

```
POST /api/auth/login
```

Example request:

```json
{
    "username": "stephen",
    "password": "password123"
}
```

The response returns an access token.

Use this token for protected routes:

```
Authorization: Bearer your_token_here
```

---

### Get Current User

```
GET /api/auth/me
```

Returns the currently logged-in user.


# Workout Routes

All workout routes require authentication.


## View Workouts

```
GET /api/workouts
```

Returns all workouts belonging to the logged-in user.


## Create Workout

```
POST /api/workouts
```

Example:

```json
{
    "exercise_name": "Bench Press",
    "duration_minutes": 45,
    "calories_burned": 300,
    "notes": "Chest workout"
}
```


## View Single Workout

```
GET /api/workouts/<id>
```


## Update Workout

```
PATCH /api/workouts/<id>
```

Example:

```json
{
    "duration_minutes": 60
}
```


## Delete Workout

```
DELETE /api/workouts/<id>
```


# Database Models

## User

Stores account details:

- id
- username
- password hash
- created date


## Workout

Stores workout information:

- id
- user id
- exercise name
- duration minutes
- calories burned
- workout date
- notes


# Technologies Used

- Python
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Marshmallow
- SQLite
- Pytest


# Project Overview

This project was built to practice backend API development using Flask.

It demonstrates:

- Building REST APIs
- User authentication
- Database relationships
- Data validation
- CRUD operations
- Automated testing

