from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required
import io

from app.services.response_clean_service import ResponseCleanService
from app.utils.response import success_response, error_response

bp = Blueprint("api_v1_response_clean", __name__, url_prefix="/api/v1/response_clean")

@bp.route("/clean/<string:response_id>", methods=["POST"]) #by uuid in response model
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

@bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    try:
        data = ResponseCleanService.get_all()

        return success_response(
            data=[d.to_dict() for d in data],
            message="Response clean list retrieved successfully"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

@bp.route("/<string:id>", methods=["GET"]) #by uuid in response clean model
@jwt_required()
def get_by_id(id):
    try:
        data = ResponseCleanService.get_by_id(id)

        if not data:
            return error_response("Data not found", 404)

        return success_response(
            data=data.to_dict(),
            message="Response clean retrieved successfully"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

@bp.route("/<string:id>", methods=["PATCH"]) #by uuid in response clean model
@jwt_required()
def update_by_id(id):
    try:

        data = request.get_json()

        description = data.get("description")
        is_wa_active = data.get("is_wa_active") or 'checking'
        propose_status = data.get("is_wa_active")

        if description is None or propose_status is None:
            return error_response("description, is_propose or is_wa_active are required", 400)

        updated = ResponseCleanService.update_description_and_status(
            id=id,
            description=description,
            propose_status=propose_status,
            is_wa_active=is_wa_active
        )

        return success_response(
            data=updated.to_dict(),
            message="Response clean updated successfully"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except ValueError as err:
        return error_response(str(err), 400)

    except Exception as err:
        return error_response(str(err), 500)

@bp.route("/<string:id>", methods=["DELETE"]) #by place in response clean model
@jwt_required()
def delete_by_id(id: str):
    try:
        deleted_count = ResponseCleanService.delete_by_id(id)

        return success_response(
            data={"deleted": deleted_count},
            message="Response clean deleted successfully"
        )

    except ValueError as err:
        return error_response(str(err), 400)

    except LookupError as err:
        return error_response(str(err), 404)

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

@bp.route("/place/<string:place_id>", methods=["PATCH"]) #by place id in response clean model
@jwt_required()
def update_by_place_id(place_id):
    try:

        data = request.get_json()

        description = data.get("description")
        is_wa_active = data.get("is_wa_active") or 'checking'
        propose_status = data.get("is_wa_active")

        if description is None or propose_status is None:
            return error_response("description, is_propose or is_wa_active are required", 400)

        updated = ResponseCleanService.update_description_and_status(
            place_id=place_id,
            description=description,
            propose_status=propose_status,
            is_wa_active=is_wa_active
        )


        return success_response(
            data=updated.to_dict(),
            message="Updated successfully"
        )
    
    except PermissionError as err:
        return error_response(str(err), 403)

    except ValueError as err:
        return error_response(str(err), 400)

    except Exception as err:
        return error_response(str(err), 400)

@bp.route("/place/<string:place_id>", methods=["GET"]) #by place id in response clean model
@jwt_required()
def get_by_place_id(place_id):
    try:
        data = ResponseCleanService.get_by_place_id(place_id)

        if not data:
            return error_response("Data not found", 404)

        return success_response(
            data=data.to_dict(),
            message="Response clean by place_id retrieved successfully"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

@bp.route("/<string:place_id>", methods=["DELETE"]) #by place in response clean model
@jwt_required()
def delete_by_place_id(place_id: str):
    try:
        deleted_count = ResponseCleanService.delete_by_place_id(place_id)

        return success_response(
            data={"deleted": deleted_count},
            message="Response clean deleted successfully"
        )

    except ValueError as err:
        return error_response(str(err), 400)

    except LookupError as err:
        return error_response(str(err), 404)

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)

@bp.route("/detail/<string:place_id>/<string:response_id>", methods=["PUT"]) #by response_id(uuid) ini response model
@jwt_required()
def update_detail(place_id, response_id):
    data = ResponseCleanService.update_from_google_detail(
        place_id=place_id,
        response_id=response_id
    )

    return success_response(
        data=data.to_dict(),
        message="Detail updated successfully"
    )

@bp.route("/export/csv", methods=["GET"])
@jwt_required()
def export_csv():
    try:
        csv_data = ResponseCleanService.export_to_csv()

        return send_file(
            io.BytesIO(csv_data.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="response_clean.csv"
        )

    except PermissionError as err:
        return error_response(str(err), 403)

    except Exception as err:
        return error_response(str(err), 500)