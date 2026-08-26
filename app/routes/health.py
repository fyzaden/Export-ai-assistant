from flask import Blueprint, jsonify
from config.config import Config


health_bp = Blueprint("health", __name__)


@health_bp.get("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "ai_provider": Config.AI_PROVIDER,
        "gemini_configured": bool(Config.GEMINI_API_KEY)
    })