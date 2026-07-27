import random
from datetime import timedelta

from faker import Faker

from app import create_app
from app.extensions import db
from app.models import User, WorkoutLog

fake = Faker()

EXERCISES = [
    "Running", "Cycling", "Swimming", "Weightlifting", "Yoga",
    "HIIT", "Pilates", "Rowing", "Boxing", "Hiking",
]


def seed():
    app = create_app()

    with app.app_context():
        print("Clearing existing data...")
        WorkoutLog.query.delete()
        User.query.delete()
        db.session.commit()

        print("Seeding users...")
        users = []
        demo_user = User(username="demo")
        demo_user.password_hash = "password123"
        db.session.add(demo_user)
        users.append(demo_user)

        for _ in range(4):
            username = fake.unique.user_name()
            user = User(username=username)
            user.password_hash = "password123"
            db.session.add(user)
            users.append(user)

        db.session.commit()

        print("Seeding workout logs...")
        for user in users:
            for _ in range(random.randint(5, 10)):
                workout = WorkoutLog(
                    user_id=user.id,
                    exercise_name=random.choice(EXERCISES),
                    duration_minutes=random.randint(15, 90),
                    calories_burned=random.randint(100, 800),
                    workout_date=fake.date_between(start_date="-60d", end_date="today"),
                    notes=fake.sentence() if random.random() > 0.4 else None,
                )
                db.session.add(workout)

        db.session.commit()

        print(f"Seeded {User.query.count()} users and {WorkoutLog.query.count()} workout logs.")
        print("Demo login -> username: 'demo', password: 'password123'")


if __name__ == "__main__":
    seed()
