from datetime import datetime

from app.extensions import db


class WorkoutLog(db.Model):
    __tablename__ = "workout_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    exercise_name = db.Column(db.String(120), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=True)
    workout_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = db.relationship("User", back_populates="workouts")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "exercise_name": self.exercise_name,
            "duration_minutes": self.duration_minutes,
            "calories_burned": self.calories_burned,
            "workout_date": self.workout_date.isoformat() if self.workout_date else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<WorkoutLog {self.id} {self.exercise_name} user={self.user_id}>"
