from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .api.v1.auth.routes import bp as api_v1_auth
from .api.v1.user.routes import bp as api_v1_user
from .api.v1.response.routes import bp as api_v1_response
from .api.v1.response_clean.routes import bp as api_v1_response_clean

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(api_v1_auth)
    app.register_blueprint(api_v1_user)
    app.register_blueprint(api_v1_response)
    app.register_blueprint(api_v1_response_clean)

    return app
