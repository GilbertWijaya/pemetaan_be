from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()  # ambil payload JWT
        if claims.get("role") != "admin":
            return jsonify({
                "status": "error",
                "message": "Admin access required"
            }), 403
        return fn(*args, **kwargs)
    return wrapper
