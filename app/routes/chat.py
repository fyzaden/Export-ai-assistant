from flask import Blueprint, jsonify, request

from app.services.ai_service import AIService


chat_bp = Blueprint("chat", __name__)

ai_service = AIService()


@chat_bp.post("/api/chat")
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Invalid JSON body"
            }), 400

        message = data.get("message", "").strip()
        conversation_history = data.get(
            "conversation_history",
            []
        )

        if not message:
            return jsonify({
                "error": "Message is required"
            }), 400

        response = ai_service.generate_response(
            message=message,
            conversation_history=conversation_history
        )

        return jsonify({
            "response": response
        })

    except Exception as e:
        print(f"Chat error: {e}")

        return jsonify({
            "error": "AI service temporarily unavailable"
        }), 500