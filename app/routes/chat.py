from flask import Blueprint, jsonify, request
import uuid

from app.services.ai_service import AIService
from database.db import (
    get_or_create_conversation,
    save_message,
    get_messages
)


chat_bp = Blueprint("chat", __name__)

ai_service = AIService()

MAX_MESSAGE_LENGTH = 4000


@chat_bp.post("/api/chat")
def chat():
    try:
        # JSON kontrolü
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        # Mesaj kontrolü
        message = data.get("message", "")

        if not isinstance(message, str):
            return jsonify({
                "error": "Message must be a string."
            }), 400

        message = message.strip()

        if not message:
            return jsonify({
                "error": "Message is required."
            }), 400

        # Mesaj uzunluğu kontrolü
        if len(message) > MAX_MESSAGE_LENGTH:
            return jsonify({
                "error": (
                    f"Message is too long. "
                    f"Maximum length is {MAX_MESSAGE_LENGTH} characters."
                )
            }), 400

        # Session kontrolü
        session_id = data.get("session_id", "")

        if not isinstance(session_id, str):
            return jsonify({
                "error": "Session ID must be a string."
            }), 400

        session_id = session_id.strip()

        # Session ID yoksa oluştur
        if not session_id:
            session_id = str(uuid.uuid4())

        # Conversation bul veya oluştur
        conversation_id = get_or_create_conversation(
            session_id
        )

        # Kullanıcı mesajını kaydet
        save_message(
            conversation_id,
            "user",
            message
        )

        # Conversation history
        conversation_history = get_messages(
            conversation_id
        )

        # Gemini
        response = ai_service.generate_response(
            message=message,
            conversation_history=conversation_history
        )

        # AI cevabını kaydet
        save_message(
            conversation_id,
            "model",
            response
        )

        return jsonify({
            "response": response,
            "session_id": session_id,
            "conversation_id": conversation_id
        }), 200

    except Exception as e:
        print(f"Chat error: {e}")

        return jsonify({
            "error": "AI service temporarily unavailable."
        }), 500