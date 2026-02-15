import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_SECRET_EXPIRED = os.getenv("JWT_SECRET_EXPIRED")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_USER = os.getenv("DB_USER")
    SQLALCHEMY_DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
    SQLALCHEMY_DATABASE_HOST = os.getenv("DB_HOST")
    SQLALCHEMY_DATABASE_PORT = os.getenv("DB_PORT")
    SQLALCHEMY_DATABASE_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_API_ALL_QUERY = os.getenv("GOOGLE_API_ALL_QUERY")
    GOOGLE_API_DETAIL_QUERY = os.getenv("GOOGLE_API_DETAIL_QUERY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
