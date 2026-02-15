
from app.models import User
from app.extensions import db

class UserRepository:

    @staticmethod
    def create(user: User):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_id(user_id: str):
        return User.query.filter_by(id=user_id).first()
    
    @staticmethod
    def all():
        return User.query.all()
    
    @staticmethod
    def update(user_id: str, fullname: str = None, username: str = None):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None

        if fullname:
            user.fullname = fullname
        if username:
            user.username = username

        db.session.commit()
        return user  # kembalikan object User
    
    @staticmethod
    def delete(user_id: str):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None

        db.session.delete(user)
        db.session.commit()
        return user  # kembalikan object User yang dihapus
