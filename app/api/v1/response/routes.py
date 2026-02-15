from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.services.response_service import ResponseService
from .schemas import ResponseCreateSchema
from app.utils.response import success_response, error_response

from app.services.google_api_service import GoogleApiService
from app.services.response_clean_service import ResponseCleanService

bp = Blueprint("api_v1_response", __name__, url_prefix="/api/v1/response")

response_schema = ResponseCreateSchema()

@bp.route("/create", methods=["POST"])
@jwt_required()
def create():
    try:
        data = request.get_json()

        prompt = data.get("prompt")
        place_id = data.get("place_id")
        parent_id = data.get("parent_id")

        # ============================
        # MODE SEARCH (Keyword)
        # ============================
        if prompt and not place_id:

            google_response = GoogleApiService.get_all_places(prompt)

            # saved = ResponseService.create(
            #     prompt=prompt,
            #     response_data=google_response,
            #     response_status="all"
            # )   

            saved = ResponseService.create(
                prompt=prompt,
                response_data=google_response,
                response_status="all"
            )

            ResponseCleanService.process_from_response_model(
                response_model=saved,
                response_status="all",
                prompt=prompt
            )

            return success_response(
                data=saved.to_dict(),
                message="Places fetched and stored successfully"
            )

        # ============================
        # MODE DETAIL (Place ID)
        # ============================
        elif place_id and parent_id:

            google_response = GoogleApiService.get_detail_place(place_id, fields=["formatted_phone_number","website"])

            # saved = ResponseService.create(
            #     prompt=place_id,
            #     response_data=google_response,
            #     parent_id=parent_id,
            #     response_status="detail"
            # )
            saved = ResponseService.create(
                prompt=place_id,
                response_data=google_response,
                parent_id=parent_id,
                response_status="detail"
            )

            ResponseCleanService.process_from_response_model(
                response_model=saved,
                response_status="detail",
                place_id=place_id
            )

            return success_response(
                data=saved.to_dict(),
                message="Place detail fetched and stored successfully"
            )

        else:
            return error_response(
                "Invalid request. Provide 'prompt' or ('place_id' and 'parent_id').",
                400
            )

    except ValidationError as err:
        return error_response(err.messages, 400)

    except PermissionError as err:
        return error_response(str(err), 403)

    except ValueError as err:
        return error_response(str(err), 404)

    except RuntimeError as err:
        return error_response(str(err), 500)

    except Exception as err:
        return error_response(str(err), 500)


# ✅ GET ALL (hanya milik user login)
@bp.route("/all", methods=["GET"])
@jwt_required()
def all_response():
    try:
        responses = ResponseService.get_all()

        return success_response(
            data=[r.to_dict() for r in responses],
            message="List of responses"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

# ✅ DETAIL
@bp.route("/detail/<string:response_id>", methods=["GET"])
@jwt_required()
def detail_by_response_id(response_id):
    try:
        response = ResponseService.get_by_id(response_id)

        if not response:
            return error_response("Response not found", 404)

        return success_response(
            data=response.to_dict(),
            message="Response detail"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)
    
# ✅ DETAIL
@bp.route("/detail/parent/<string:parent_id>", methods=["GET"])
@jwt_required()
def detail_by_parent_id(parent_id):
    try:
        response = ResponseService.get_by_parent_id(parent_id)

        if not response:
            return error_response("Response not found", 404)

        return success_response(
            data=response.to_dict(),
            message="Response detail"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

# ✅ GET BY PROMPT (place_id atau keyword)
@bp.route("/by-prompt", methods=["GET"])
@jwt_required()
def get_by_prompt():
    try:
        place_id = request.args.get("place_id")
        keyword = request.args.get("keyword")

        # Validasi: hanya boleh salah satu
        if bool(place_id) == bool(keyword):
            return error_response(
                "Provide either place_id or keyword, not both.",
                400
            )

        response = ResponseService.get_by_prompt(
            place_id=place_id,
            keyword=keyword
        )

        if not response:
            return error_response("Response not found", 404)

        return success_response(
            data=response.to_dict(),
            message="Response found"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except ValueError as err:
        return error_response(str(err), 400)

    except Exception as err:
        return error_response(str(err), 500)

# ✅ DELETE
@bp.route("/delete/<string:response_id>", methods=["DELETE"])
@jwt_required()
def delete(response_id):
    try:
        response = ResponseService.delete(response_id)

        if not response:
            return error_response("Response not found", 404)

        return success_response(
            data=response.to_dict(),
            message="Response deleted successfully"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)
