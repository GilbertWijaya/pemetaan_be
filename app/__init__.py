from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .api.v1.auth.routes import bp as api_v1_auth
from .api.v1.user.routes import bp as api_v1_user
from .api.v1.response.routes import bp as api_v1_response
from .api.v1.response_clean.routes import bp as api_v1_response_clean
from .api.v1.health import bp as api_v1_health
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # jwt
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_SECRET_EXPIRED"] = Config.JWT_SECRET_EXPIRED

    # CORS
    CORS(app, resources={r"/api/v1/*" : {"origins": ["http://localhost:5173", "https://leads-fe-v1.vercel.app"]}})

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprints
    for bp, prefix in [
        (api_v1_auth, "/api/v1/auth"),
        (api_v1_user, "/api/v1/user"),
        (api_v1_response, "/api/v1/response"),
        (api_v1_response_clean, "/api/v1/response_clean"),
        (api_v1_health, "/")
    ]: app.register_blueprint(bp, url_prefix=prefix)

    return app
