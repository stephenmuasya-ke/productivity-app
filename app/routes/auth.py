from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import SignupSchema, LoginSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

signup_schema = SignupSchema()
login_schema = LoginSchema()


@auth_bp.route("/signup", methods=["POST"])
def signup():
    json_data = request.get_json(silent=True) or {}

    try:
        data = signup_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username is already taken"}), 422

    user = User(username=data["username"])
    user.password_hash = data["password"]

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    return (
        jsonify({"user": user.to_dict(), "access_token": access_token}),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    json_data = request.get_json(silent=True) or {}

    try:
        data = login_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.authenticate(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"user": user.to_dict(), "access_token": access_token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200
