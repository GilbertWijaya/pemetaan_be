from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.services.response_clean_service import ResponseCleanService
from app.utils.response import success_response, error_response

bp = Blueprint("api_v1_response_clean", __name__, url_prefix="/api/v1/response_clean")

@bp.route("/clean/<string:response_id>", methods=["POST"])
@jwt_required()
def generate_clean(response_id):
    try:
        created = ResponseCleanService.process_by_response_id(response_id)

        return success_response(
            data=[c.to_dict() for c in created],
            message="Clean data generated successfully"
        )

    except Exception as err:
        return error_response(str(err), 500)
