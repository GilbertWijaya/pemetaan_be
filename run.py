from flask import Flask
# from app.extensions import db, migrate, jwt
from app.config import Config
from flask_jwt_extended import JWTManager
from app.middlewares.error_handler import error_handlers
from app import create_app
import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# jwt = JWTManager()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
#     app.config["JWT_SECRET_EXPIRED"] = Config.JWT_SECRET_EXPIRED

#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
    
#     error_handlers(app)

#     return app


app = create_app()

# with app.app_context():
#     db.engine.connect()
#     print("Database connected!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
