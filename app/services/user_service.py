from app.repositories.user_repository import UserRepository
from flask_jwt_extended import get_jwt_identity

class UserService:
    
    @staticmethod
    def all(): 
        return UserRepository.all()

    @staticmethod
    def update(fullname: str = None, username: str = None):
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(user_id)

        if not user:
            return None

        # update menggunakan repository
        updated_user = UserRepository.update(user_id, fullname=fullname, username=username)

        # kembalikan object User
        return updated_user

    
    @staticmethod
    def delete(delete_id: str):
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(delete_id)

        if not user or not user_id:
            return None

        # simpan object sebelum dihapus
        deleted_user = user

        # hapus user
        UserRepository.delete(delete_id)

        # kembalikan object User yang dihapus
        return deleted_user


