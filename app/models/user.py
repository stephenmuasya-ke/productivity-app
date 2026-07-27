from datetime import datetime

from app.extensions import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    _password_hash = db.Column("password_hash", db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    workouts = db.relationship(
        "WorkoutLog",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    @property
    def password_hash(self):
        raise AttributeError("password_hash is not directly readable")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.id} {self.username}>"
