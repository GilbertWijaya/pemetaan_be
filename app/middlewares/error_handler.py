from flask import jsonify
from app.utils.exceptions import BadRequest

def error_handlers(app):

    @app.errorhandler(BadRequest)
    def bad_request(e):
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "status": "error",
            "message": "Not Found"
        }), 404
