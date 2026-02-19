from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt
from app.api.v1.auth.routes import bp as api_v1_auth
from app.api.v1.user.routes import bp as api_v1_user
from app.api.v1.response.routes import bp as api_v1_response
from app.api.v1.response_clean.routes import bp as api_v1_response_clean
from app.api.v1.health import bp as api_v1_health
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_SECRET_EXPIRED"] = Config.JWT_SECRET_EXPIRED

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(api_v1_auth)
    app.register_blueprint(api_v1_user)
    app.register_blueprint(api_v1_response)
    app.register_blueprint(api_v1_response_clean)
    app.register_blueprint(api_v1_health)

    return app
