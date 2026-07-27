from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.workout import WorkoutLog
from app.schemas.workout_schema import WorkoutLogSchema, WorkoutLogUpdateSchema

workouts_bp = Blueprint("workouts", __name__, url_prefix="/api/workouts")

create_schema = WorkoutLogSchema()
update_schema = WorkoutLogUpdateSchema()


def _get_owned_workout_or_error(workout_id, user_id):
    """Fetch a workout by id, enforcing that it belongs to user_id.

    Returns (workout, error_response). Exactly one of them is None.
    Not-found and not-owned both return 404, so ownership is never leaked.
    """
    workout = WorkoutLog.query.get(workout_id)

    if not workout or workout.user_id != int(user_id):
        return None, (jsonify({"error": "Workout log not found"}), 404)

    return workout, None


@workouts_bp.route("", methods=["GET"])
@jwt_required()
def index():
    user_id = get_jwt_identity()

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    try:
        per_page = int(request.args.get("per_page", current_app.config["DEFAULT_PAGE_SIZE"]))
    except ValueError:
        per_page = current_app.config["DEFAULT_PAGE_SIZE"]

    page = max(page, 1)
    per_page = max(1, min(per_page, current_app.config["MAX_PAGE_SIZE"]))

    pagination = (
        WorkoutLog.query.filter_by(user_id=int(user_id))
        .order_by(WorkoutLog.workout_date.desc(), WorkoutLog.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return (
        jsonify(
            {
                "workouts": [w.to_dict() for w in pagination.items],
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            }
        ),
        200,
    )


@workouts_bp.route("", methods=["POST"])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}

    try:
        data = create_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    workout = WorkoutLog(
        user_id=int(user_id),
        exercise_name=data["exercise_name"],
        duration_minutes=data["duration_minutes"],
        calories_burned=data.get("calories_burned"),
        workout_date=data.get("workout_date") or datetime.utcnow().date(),
        notes=data.get("notes"),
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify({"workout": workout.to_dict()}), 201


@workouts_bp.route("/<int:workout_id>", methods=["GET"])
@jwt_required()
def show(workout_id):
    user_id = get_jwt_identity()
    workout, error = _get_owned_workout_or_error(workout_id, user_id)

    if error:
        return error

    return jsonify({"workout": workout.to_dict()}), 200


@workouts_bp.route("/<int:workout_id>", methods=["PATCH", "PUT"])
@jwt_required()
def update(workout_id):
    user_id = get_jwt_identity()
    workout, error = _get_owned_workout_or_error(workout_id, user_id)

    if error:
        return error

    json_data = request.get_json(silent=True) or {}

    try:
        data = update_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    for field, value in data.items():
        setattr(workout, field, value)

    db.session.commit()

    return jsonify({"workout": workout.to_dict()}), 200


@workouts_bp.route("/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete(workout_id):
    user_id = get_jwt_identity()
    workout, error = _get_owned_workout_or_error(workout_id, user_id)

    if error:
        return error

    db.session.delete(workout)
    db.session.commit()

    return jsonify({}), 204
