from flask import Blueprint, jsonify, request

from database.db import create_lead


leads_bp = Blueprint("leads", __name__)


@leads_bp.post("/api/leads")
def create_lead_route():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        # Ad Soyad
        name = data.get("name", "")

        if not isinstance(name, str):
            return jsonify({
                "error": "Name must be a string."
            }), 400

        name = name.strip()

        if not name:
            return jsonify({
                "error": "Name is required."
            }), 400

        # Telefon
        phone = data.get("phone", "")

        if not isinstance(phone, str):
            return jsonify({
                "error": "Phone must be a string."
            }), 400

        phone = phone.strip()

        if not phone:
            return jsonify({
                "error": "Phone is required."
            }), 400

        # Firma
        company = data.get("company", "")

        if not isinstance(company, str):
            return jsonify({
                "error": "Company must be a string."
            }), 400

        company = company.strip()

        # Mesaj
        message = data.get("message", "")

        if not isinstance(message, str):
            return jsonify({
                "error": "Message must be a string."
            }), 400

        message = message.strip()

        # Session ID
        session_id = data.get("session_id", "")

        if not isinstance(session_id, str):
            return jsonify({
                "error": "Session ID must be a string."
            }), 400

        session_id = session_id.strip()

        # Lead'i database'e kaydet
        lead_id = create_lead(
            name=name,
            phone=phone,
            company=company,
            message=message,
            session_id=session_id
        )

        return jsonify({
            "status": "success",
            "lead_id": lead_id
        }), 201

    except Exception as e:
        print(f"Lead error: {e}")

        return jsonify({
            "error": "Lead could not be created."
        }), 500