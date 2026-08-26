from flask import Blueprint, jsonify, request

from app.services.ai_service import AIService


chat_bp = Blueprint("chat", __name__)

ai_service = AIService()


@chat_bp.post("/api/chat")
def chat():
    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    response = ai_service.generate_response(message)

    return jsonify({
        "response": response
    })