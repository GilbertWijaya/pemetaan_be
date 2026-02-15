from typing import List, Optional
from app.models import Response
from app.extensions import db

class ResponseRepository:

    @staticmethod
    def create(response: Response):
        db.session.add(response)
        db.session.commit()
        return response
    
    @staticmethod
    def create_bulk(responses: List[Response]) -> List[Response]:
        db.session.add_all(responses)
        db.session.commit()
        return responses

    @staticmethod
    def get_by_id(response_id: str):
        return Response.query.filter_by(id=response_id).first()

    @staticmethod
    def get_by_parent_id(parent_id: str):
        return Response.query.filter_by(parent_id=parent_id).first()
    
    @staticmethod
    def get_by_prompt(place_id: str = None, keyword: str = None):
        if place_id:
            return Response.query.filter_by(prompt=place_id).first()
        
        elif keyword: 
            return Response.query.filter_by(prompt=keyword).first()
        
        elif (not place_id and not keyword) or (place_id and keyword):
            raise ValueError("Provide either place_id or keyword, not both.")       

    
    @staticmethod
    def all():
        return Response.query.all()
    
    @staticmethod
    def delete(response_id: str):
        response = ResponseRepository.get_by_id(response_id)
        if not response:
            return None

        db.session.delete(response)
        db.session.commit()
        return response
