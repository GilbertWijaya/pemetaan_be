# from typing import Optional, List
# from flask_jwt_extended import get_jwt_identity

# from app.extensions import db
# from app.models.response_clean import ResponseClean
# from app.models.response import Response
# from app.utils.mapping_response import map_data


# class ResponseCleanService:

#     # ==========================================================
#     # AUTO PROCESS (dipanggil dari route create)
#     # ==========================================================
#     @staticmethod
#     def process_from_response_model(
#         response_model: Response,
#         response_status: str,
#         prompt: Optional[str] = None,
#         place_id: Optional[str] = None,
#     ) -> List[ResponseClean]:

#         user_id = get_jwt_identity()
#         raw_data = response_model.response_data
#         cleaned_records = []

#         # ===============================
#         # MODE SEARCH
#         # ===============================
#         if response_status == "all":

#             mapped_results = map_data(
#                 data=raw_data,
#                 prompt=prompt,
#                 detail=False
#             )

#             for item in mapped_results:

#                 # Hindari duplicate
#                 existing = ResponseClean.query.filter_by(
#                     place_id=item.get("place_id"),
#                     response_id=response_model.id
#                 ).first()

#                 if existing:
#                     continue

#                 clean = ResponseClean(
#                     place_id=item.get("place_id"),
#                     place_name=item.get("name"),
#                     format_address={
#                         "formatted_address": item.get("formatted_address")
#                     },
#                     geometry=item.get("geometry"),
#                     formatted_phone_number={},
#                     rating=item.get("rating") or 0,
#                     user_rating_total=item.get("total_reviews") or 0,
#                     business_status=item.get("business_status") or "UNKNOWN",
#                     categorical=",".join(item.get("types", [])),
#                     industry_type=item.get("types")[0] if item.get("types") else "unknown",
#                     other_data=item,
#                     description=f"Generated from keyword: {prompt}",
#                     user_id=user_id,
#                     response_id=response_model.id
#                 )

#                 db.session.add(clean)
#                 cleaned_records.append(clean)

#         # ===============================
#         # MODE DETAIL
#         # ===============================
#         elif response_status == "detail":

#             mapped_results = map_data(
#                 data=raw_data,
#                 place_id=place_id,
#                 detail=True
#             )

#             if not mapped_results:
#                 return []

#             detail_data = mapped_results[0]

#             # Cari parent clean
#             existing = ResponseClean.query.filter_by(
#                 place_id=place_id,
#                 response_id=response_model.parent_id
#             ).first()

#             if existing:
#                 existing.formatted_phone_number = {
#                     "formatted_phone_number": detail_data.get("formatted_phone_number"),
#                     "website": detail_data.get("website"),
#                 }

#                 existing.description += " | Detail metadata updated"
#                 db.session.add(existing)
#                 cleaned_records.append(existing)

#         db.session.commit()
#         return cleaned_records


#     # ==========================================================
#     # MANUAL PROCESS BY RESPONSE ID
#     # ==========================================================
#     @staticmethod
#     def process_by_response_id(response_id: str) -> List[ResponseClean]:
#         """
#         Generate clean data secara manual dari response yang sudah ada di DB
#         """

#         user_id = get_jwt_identity()

#         response_model = Response.query.filter_by(
#             id=response_id,
#             user_id=user_id
#         ).first()

#         if not response_model:
#             raise ValueError("Response not found or unauthorized")

#         return ResponseCleanService.process_from_response_model(
#             response_model=response_model,
#             response_status=response_model.response_status,
#             prompt=response_model.prompt,
#             place_id=response_model.prompt
#         )


#     # ==========================================================
#     # MANUAL REBUILD ALL USER RESPONSES
#     # ==========================================================
#     @staticmethod
#     def rebuild_all_user_clean_data() -> int:
#         """
#         Rebuild semua clean data milik user login
#         """

#         user_id = get_jwt_identity()

#         responses = Response.query.filter_by(user_id=user_id).all()

#         total_created = 0

#         for response in responses:
#             results = ResponseCleanService.process_from_response_model(
#                 response_model=response,
#                 response_status=response.response_status,
#                 prompt=response.prompt,
#                 place_id=response.prompt
#             )

#             total_created += len(results)

#         return total_created


#     # ==========================================================
#     # DELETE CLEAN BY RESPONSE
#     # ==========================================================
#     @staticmethod
#     def delete_by_response_id(response_id: str) -> int:

#         user_id = get_jwt_identity()

#         records = ResponseClean.query.filter_by(
#             response_id=response_id,
#             user_id=user_id
#         ).all()

#         count = len(records)

#         for record in records:
#             db.session.delete(record)

#         db.session.commit()
#         return count

from typing import Optional, List
from flask_jwt_extended import get_jwt_identity

from app.models.response_clean import ResponseClean
from app.repositories.response_repository import ResponseRepository
from app.repositories.response_clean_repository import ResponseCleanRepository
from app.utils.mapping_response import map_data


class ResponseCleanService:

    # ==========================================================
    # AUTO PROCESS (dipanggil setelah response/create)
    # ==========================================================
    @staticmethod
    def process_from_response_model(
        response_model,
        response_status: str,
        prompt: Optional[str] = None,
        place_id: Optional[str] = None,
    ) -> List[ResponseClean]:

        user_id = get_jwt_identity()
        raw_data = response_model.response
        cleaned_records = []

        # ===============================
        # MODE SEARCH
        # ===============================
        if response_status == "all":

            mapped_results = map_data(
                data=raw_data,
                prompt=prompt,
                detail=False
            )

            for item in mapped_results:

                # Anti duplicate
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
                    description=f"Generated from keyword: {prompt}",
                    user_id=user_id,
                    response_id=response_model.id
                )

                cleaned_records.append(clean)

            if cleaned_records:
                ResponseCleanRepository.create_bulk(cleaned_records)

        # ===============================
        # MODE DETAIL
        # ===============================
        elif response_status == "detail":

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
                existing.formatted_phone_number = {
                    "formatted_phone_number": detail_data.get("formatted_phone_number"),
                    "website": detail_data.get("website"),
                }

                existing.description += " | Detail metadata updated"

                ResponseCleanRepository.create(existing)
                cleaned_records.append(existing)

        return cleaned_records


    # ==========================================================
    # MANUAL PROCESS BY RESPONSE ID
    # ==========================================================
    @staticmethod
    def process_by_response_id(response_id: str) -> List[ResponseClean]:

        user_id = get_jwt_identity()

        response_model = ResponseRepository.get_by_id(response_id)

        if not response_model:
            raise ValueError("Response not found")

        if str(response_model.user_id) != str(user_id):
            raise PermissionError("Unauthorized access")

        return ResponseCleanService.process_from_response_model(
            response_model=response_model,
            response_status=response_model.response_status,
            prompt=response_model.prompt,
            place_id=response_model.prompt
        )


    # ==========================================================
    # REBUILD ALL USER CLEAN DATA
    # ==========================================================
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


    # ==========================================================
    # DELETE CLEAN BY RESPONSE
    # ==========================================================
    @staticmethod
    def delete_by_response_id(response_id: str) -> int:

        response = ResponseRepository.get_by_id(response_id)

        if not response:
            raise ValueError("Response not found")

        return ResponseCleanRepository.delete_by_response_id(response_id)
