from typing import List, Optional
from app.models.response_clean import ResponseClean
from app.extensions import db

class ResponseCleanRepository:

    @staticmethod
    def create(clean: ResponseClean) -> ResponseClean:
        db.session.add(clean)
        db.session.commit()
        return clean

    @staticmethod
    def create_bulk(cleans: List[ResponseClean]) -> List[ResponseClean]:
        db.session.add_all(cleans)
        db.session.commit()
        return cleans

    @staticmethod
    def get_all():
        return ResponseClean.query.all()
    
    @staticmethod
    def get_by_id(id: str):
        # return ResponseClean.query.filter_by(id=id)
        return ResponseClean.query.filter_by(id=id).first()

    @staticmethod
    def get_by_place_id(place_id: str):
        return ResponseClean.query.filter_by(place_id=place_id)

    @staticmethod
    def get_by_place_and_response(place_id: str, response_id: str) -> Optional[ResponseClean]: #by response_id(uuid) in response model
        return ResponseClean.query.filter_by(
            place_id=place_id,
            response_id=response_id
        ).first()

    @staticmethod
    def get_by_response_id(response_id: str) -> List[ResponseClean]: #by response_id(uuid) in response model
        return ResponseClean.query.filter_by(response_id=response_id).all()
    
    @staticmethod
    def update() -> None:
        db.session.commit()


    @staticmethod
    def delete_by_response_id(response_id: str) -> int:
        records = ResponseClean.query.filter_by(response_id=response_id).all()
        count = len(records)

        for record in records:
            db.session.delete(record)

        db.session.commit()
        return count
    
    @staticmethod
    def delete_by_place_id(place_id: str) -> int:
        if not place_id:
            raise ValueError("place_id is required")

        deleted_count = ResponseClean.query.filter_by(
            place_id=place_id
        ).delete()

        db.session.commit()

        return deleted_count
    
    @staticmethod
    def delete_by_id(id: str) -> int:
        if not id:
            raise ValueError("id is required")

        deleted_count = ResponseClean.query.filter_by(
            id
        ).delete()

        db.session.commit()

        return deleted_count

