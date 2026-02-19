
from flask import Blueprint

bp = Blueprint("api_v1_health", __name__, url_prefix="/")

@bp.route('/')
def health_check():
    return {"status": "healthy", "message": "Backend Peta is running"}, 200