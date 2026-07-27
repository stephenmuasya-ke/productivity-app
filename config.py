import os
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY",
        "productivity-workout-api-super-secret-key-2026"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ["headers"]


    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Pagination Configuration
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 50
