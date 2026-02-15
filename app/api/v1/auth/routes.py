from flask import Blueprint, request
from marshmallow import ValidationError
from app.services.auth_service import AuthService
from app.api.v1.auth.schemas import AuthLoginSchema, AuthRegisterSchema
from app.utils.response import success_response, error_response
from flask_jwt_extended import jwt_required

bp = Blueprint("api_v1_auth", __name__, url_prefix="/api/v1/auth")

login_schema = AuthLoginSchema()
register_schema = AuthRegisterSchema()


@bp.route("/register", methods=["POST"])
def register():
    json_data = request.get_json()

    if not json_data:
        return error_response("Request body is required", 400)

    try:
        data = register_schema.load(json_data)  # 🔥 validasi otomatis

        AuthService.register(
            data["fullname"],
            data["username"],
            data["email"],
            data["password"],
            data["role"]
        )

        return success_response(data, "User registered")

    except ValidationError as err:
        return error_response(err.messages, 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route("/login", methods=["POST"])
def login():
    json_data = request.get_json()

    if not json_data:
        return error_response("Request body is required", 400)

    try:
        data = login_schema.load(json_data)  # 🔥 validasi otomatis

        result = AuthService.login(
            data["email"],
            data["password"]
        )

        return success_response(result, "Login successful")

    except ValidationError as err:
        return error_response(err.messages, 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = AuthService.me()
    if not user:
        return error_response("User not found", 404)
    return success_response(user, "Current user info")
