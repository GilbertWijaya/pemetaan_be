from typing import Optional, List
from flask_jwt_extended import get_jwt_identity

import csv, io

from app.models.response_clean import ResponseClean
from app.repositories.response_repository import ResponseRepository
from app.repositories.response_clean_repository import ResponseCleanRepository
from app.utils.mapping_response import map_data
from app.services.google_api_service import GoogleApiService
from app.utils.phone_number_helper import validate_and_format_phone

class ResponseCleanService:

    @staticmethod
    def process_from_response_model(
        response_model,
        response_status: str,
        prompt: Optional[str] = None,
        place_id: Optional[str] = None,
    ) -> List[ResponseClean]:

        raw_data = response_model.response
        cleaned_records = []

        # MODE SEARCH
        if response_status == "all":

            mapped_results = map_data(
                data=raw_data,
                prompt=prompt,
                detail=False
            )

            for item in mapped_results:

                existing = ResponseCleanRepository.get_by_place_and_response(
                    place_id=item.get("place_id"),
                    response_id=response_model.id
                )

                if existing:
                    continue

                clean = ResponseClean(
                    place_id=item.get("place_id"),
                    place_name=item.get("name"),
                    format_address={
                        "formatted_address": item.get("formatted_address")
                    },
                    geometry=item.get("geometry"),
                    formatted_phone_number={},
                    rating=item.get("rating") or 0,
                    user_rating_total=item.get("total_reviews") or 0,
                    business_status=item.get("business_status") or "UNKNOWN",
                    categorical=",".join(item.get("types", [])),
                    industry_type=item.get("types")[0] if item.get("types") else "unknown",
                    other_data=item,
                    description="",  # ← dikosongkan
                    user_id=response_model.user_id,
                    response_id=response_model.id
                )

                cleaned_records.append(clean)

            if cleaned_records:
                ResponseCleanRepository.create_bulk(cleaned_records)

        # MODE DETAIL
        elif response_status == "detail":

            if not response_model.parent_id:
                raise ValueError("Detail response must have parent_id")

            mapped_results = map_data(
                data=raw_data,
                place_id=place_id,
                detail=True
            )

            if not mapped_results:
                return []

            detail_data = mapped_results[0]

            existing = ResponseCleanRepository.get_by_place_and_response(
                place_id=place_id,
                response_id=response_model.parent_id
            )

            if existing:

                # Update phone only
                existing.formatted_phone_number = {
                    "formatted_phone_number": detail_data.get("formatted_phone_number")
                }

                # Merge website ke other_data
                current_other = existing.other_data or {}
                current_other["website"] = detail_data.get("website")
                existing.other_data = current_other

                # description tidak disentuh
                ResponseCleanRepository.create(existing)
                cleaned_records.append(existing)

        return cleaned_records

    @staticmethod
    def update_from_google_detail(place_id: str):

        if not place_id:
            raise ValueError("place_id is required")

        # if not response_id:
        #     raise ValueError("response_id is required")

        # Ambil data dari database
        # existing = ResponseCleanRepository.get_by_place_and_response(
        #     place_id=place_id,
        #     response_id=response_id
        # )
        existing = ResponseCleanRepository.get_by_place_id(
            place_id=place_id,
        )

        if not existing:
            raise ValueError("ResponseClean not found")

        # Panggil Google Detail API
        detail_response = GoogleApiService.get_detail_place(place_id)

        if detail_response.get("status") != "OK":
            raise RuntimeError("Google detail API returned invalid status")

        result = detail_response.get("result", {})

        phone_raw = result.get("formatted_phone_number")

        # Validasi & Normalisasi Phone
        phone_result = validate_and_format_phone(phone_raw)

        # Update formatted_phone_number (raw)
        existing.formatted_phone_number = {
            "formatted_phone_number": phone_raw
        }

        # Update is_wa_active berdasarkan helper
        existing.is_wa_active = phone_result["is_wa_active"]

        existing.other_data = {
            "website": result.get("website"),
            "url": f'https://www.google.com/maps/place/?q=place_id:{place_id}',
            "phone_normalized": phone_result["normalized_phone"],
            "wa_link": phone_result["wa_link"]
        }

        ResponseCleanRepository.update()

        return existing

    # MANUAL PROCESS BY RESPONSE ID
    @staticmethod
    def process_by_response_id(response_id: str) -> List[ResponseClean]:

        user_id = get_jwt_identity()

        response_model = ResponseRepository.get_by_id(response_id)

        if not response_model:
            raise ValueError("Response not found")

        # if str(response_model.user_id) != str(user_id):
        #     raise PermissionError("Unauthorized access")

        return ResponseCleanService.process_from_response_model(
            response_model=response_model,
            response_status=response_model.response_status,
            prompt=response_model.prompt,
            place_id=response_model.prompt
        )

    # REBUILD ALL USER CLEAN DATA
    @staticmethod
    def rebuild_all_user_clean_data() -> int:

        user_id = get_jwt_identity()
        responses = ResponseRepository.all()

        total_created = 0

        for response in responses:
            if str(response.user_id) != str(user_id):
                continue

            results = ResponseCleanService.process_from_response_model(
                response_model=response,
                response_status=response.response_status,
                prompt=response.prompt,
                place_id=response.prompt
            )

            total_created += len(results)

        return total_created

    @staticmethod
    def get_all():
        user_id = get_jwt_identity()

        if not user_id:
            raise PermissionError("Unauthorized")
        
        return ResponseCleanRepository.get_all()
    
    @staticmethod
    def get_by_id(id:str):
        user_id = get_jwt_identity()

        if not user_id:
            raise PermissionError("Unauthorized")
        
        return ResponseCleanRepository.get_by_id(id)
    
    @staticmethod
    def update_description_and_status(id: str, description: str, propose_status: str, is_wa_active: str ): 

        user_id = get_jwt_identity()

        if not user_id:
            raise PermissionError("Unauthorized")

        clean = ResponseCleanRepository.get_by_id(id)

        if not clean:
            raise ValueError("ResponseClean not found")

        # if str(clean.user_id) != str(user_id):
        #     raise PermissionError("Forbidden access")

        # Validasi ENUM manual
        allowed_status = ['propose', 'reject', 'checking']
        allowed_wa_checking = ['checking', 'active', 'non-active']

        if propose_status not in allowed_status:
            raise ValueError(f"Invalid propose status. Allowed: {allowed_status}")
        
        if is_wa_active not in allowed_wa_checking:
            raise ValueError(f"Invalid propose status. Allowed: {allowed_wa_checking}")

        # Update field
        clean.description = description
        clean.is_propose = propose_status
        clean.is_wa_active = is_wa_active

        ResponseCleanRepository.update()

        return clean

    @staticmethod
    def update_description_and_status(place_id: str, description: str, propose_status: str,  is_wa_active: str):

        user_id = get_jwt_identity()

        if not user_id:
            raise PermissionError("Unauthorized")

        clean = ResponseCleanRepository.get_by_place_id(place_id)

        if not clean:
            raise ValueError("ResponseClean not found")

        # clean = clean.first()

        # if str(clean.user_id) != str(user_id):
        #     raise PermissionError("Forbidden access")

        allowed_status = ['propose', 'reject', 'checking']
        allowed_wa_checking = ['checking', 'active', 'non-active']

        if propose_status not in allowed_status:
            raise ValueError("Invalid propose status")
        if is_wa_active not in allowed_wa_checking:
            raise ValueError(f"Invalid propose status. Allowed: {allowed_wa_checking}")

        clean.description = description
        clean.is_propose = propose_status
        clean.is_wa_active = is_wa_active

        ResponseCleanRepository.update()

        return clean

    @staticmethod
    def get_by_place_id(place_id:str):
        user_id = get_jwt_identity()

        if not user_id:
            raise PermissionError("Unauthorized")
        
        return ResponseCleanRepository.get_by_place_id(place_id)

    # DELETE CLEAN BY RESPONSE
    @staticmethod
    def delete_by_response_id(response_id: str) -> int:

        response = ResponseRepository.get_by_id(response_id)

        if not response:
            raise ValueError("Response not found")

        return ResponseCleanRepository.delete_by_response_id(response_id)

    @staticmethod
    def delete_by_place_id(place_id: str) -> int:
        if not place_id:
            raise ValueError("place_id is required")

        deleted_count = ResponseCleanRepository.delete_by_place_id(place_id)

        if deleted_count == 0:
            raise LookupError("No data found for this place_id")

        return deleted_count
    
    def delete_by_id(id: str) -> int:
        if not id:
            raise ValueError("id is required")

        deleted_count = ResponseCleanRepository.delete_by_id(id)

        if deleted_count == 0:
            raise LookupError("No data found for this id")

        return deleted_count

    @staticmethod
    def export_to_csv():

        user_id = get_jwt_identity()

        if not user_id:
            raise PermissionError("Unauthorized")

        records = ResponseCleanRepository.get_all()

        # Filter berdasarkan user
        records = [r for r in records]

        output = io.StringIO()
        writer = csv.writer(output)

        # Header CSV
        writer.writerow([
            "id",
            "place_id",
            "place_name",
            "formatted_address",
            "formatted_phone_number"
            "rating",
            "total_reviews",
            "business_status",
            "industry_type",
            "is_propose",
            "description",
            "other_data",
            "created_at"
        ])

        for r in records:
            writer.writerow([
                r.id,
                r.place_id,
                r.place_name,
                (r.format_address or {}).get("formatted_address"),
                (r.formatted_phone_number or {}).get("formatted_phone_number"),
                r.rating,
                r.user_rating_total,
                r.business_status,
                r.industry_type,
                r.is_propose,
                r.description,
                (r.other_data or {}).get("other_data"),
                r.created_at
            ])

        output.seek(0)
        return output
