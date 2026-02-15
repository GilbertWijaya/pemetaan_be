
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.user_service import UserService
from app.utils.response import success_response, error_response

bp = Blueprint("api_v1_user", __name__, url_prefix="/api/v1/user")

@bp.route("/all", methods=["GET"])
@jwt_required()
def all_users():
    users = UserService.all()
    if not users:
        return error_response(message="user not found", code=404)
    
    # pastikan semua user diubah ke dict
    users_data = [user.to_dict() for user in users]
    return success_response(users_data, "All users retrieved successfully")

@bp.route("/update", methods=["PATCH"])
@jwt_required()
def update_user():
    data = request.get_json() or {}
    fullname = data.get("fullname")
    username = data.get("username")

    if not fullname and not username:
        return error_response("Nothing to update", 400)

    updated_user = UserService.update(fullname=fullname, username=username)

    if not updated_user:
        return error_response("User not found", 404)

    # pastikan dikembalikan sebagai dict
    return success_response(updated_user.to_dict(), "User updated successfully")

@bp.route("/delete/<string:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # panggil service dengan id dari URL
    deleted_user = UserService.delete(user_id)

    if not deleted_user:
        return error_response("User not found", 404)

    return success_response(deleted_user.to_dict(), "User deleted successfully")
