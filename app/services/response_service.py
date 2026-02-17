from flask_jwt_extended import get_jwt_identity
from app.models import Response
from app.repositories.response_repository import ResponseRepository
from app.extensions import db

class ResponseService:

    @staticmethod
    def create(prompt: str, response_data: dict, parent_id: str = None, response_status: str= "all"):
        current_user_id = get_jwt_identity()

        # service ini ambil query dan parent id jika diperlukan lal gunakan google place api untuk ambil semua data

        if not current_user_id:
            raise PermissionError("Unauthorized")

        # Validasi parent hanya jika dikirim
        if parent_id:
            parent = ResponseRepository.get_by_id(parent_id)

            if not parent:
                raise ValueError("Parent response not found")

            if str(parent.user_id) != str(current_user_id):
                raise PermissionError("Parent does not belong to you")

        new_response = Response(
            prompt=prompt,
            response=response_data,
            response_status=response_status,
            user_id=current_user_id,
            parent_id= parent_id  # otomatis None kalau tidak dikirim
        )

        return ResponseRepository.create(new_response)

    @staticmethod
    def get_by_id(response_id: str):
        current_user_id = get_jwt_identity()

        if not current_user_id:
            raise PermissionError("Unauthorized")

        response = ResponseRepository.get_by_id(response_id)

        if not response:
            return None

        if str(response.user_id) != str(current_user_id):
            raise PermissionError("Forbidden")

        return response

    @staticmethod
    def get_by_parent_id(parent_id: str):
        current_user_id = get_jwt_identity()

        if not current_user_id:
            raise PermissionError("Unauthorized")

        response = ResponseRepository.get_by_parent_id(parent_id)

        if not response:
            return None

        return response
    
    @staticmethod
    def get_by_prompt(place_id: str, keyword: str):
        current_user_id = get_jwt_identity()

        if not current_user_id:
            raise PermissionError("Unauthorized")

        if place_id:
            return ResponseRepository.get_by_prompt(place_id=place_id)
        elif keyword:
            return ResponseRepository.get_by_prompt(keyword=keyword)

        if (not place_id and not keyword) or (place_id and keyword):
            raise ValueError("Provide either place_id or keyword, not both.")

    @staticmethod
    def get_all():
        current_user_id = get_jwt_identity()

        if not current_user_id:
            raise PermissionError("Unauthorized")

        return ResponseRepository.all()

    @staticmethod
    def delete(response_id: str):
        current_user_id = get_jwt_identity()

        if not current_user_id:
            raise PermissionError("Unauthorized")

        response = ResponseRepository.get_by_id(response_id)

        if not response:
            return None

        if str(response.user_id) != str(current_user_id):
            raise PermissionError("Forbidden")

        db.session.delete(response)
        db.session.commit()

        return response
