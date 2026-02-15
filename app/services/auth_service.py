from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import get_jwt_identity
from app.utils.response import error_response

class AuthService:

    @staticmethod
    def register(fullname: str, username: str, email: str, password: str, role: str = "user"):
        # cek email sudah ada atau belum
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = generate_password_hash(password)

        user = User(
            fullname=fullname,
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        data = UserRepository.create(user)
        return data
        

    @staticmethod
    def login(email: str, password: str):
        user = UserRepository.get_by_email(email)

        if not user:
            return error_response("user not found", 404)

        if not check_password_hash(user.password, password):
            return error_response("sorry wrong password", 400)

        # buat JWT token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "email": user.email,
                "role": user.role
            }
        )

        refresh_token = create_refresh_token(identity=user.id)

        return {
            "user_id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "role": user.role,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def me():
        user_id = get_jwt_identity()

        user = UserRepository.get_by_id(user_id)
        if not user:
            return None  # jangan return error_response di sini

        return user.to_dict()

