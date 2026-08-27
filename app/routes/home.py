from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__)


@home_bp.get("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "export-ai-assistant",
        "message": "Export AI Assistant API is running"
    })