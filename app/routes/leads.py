from flask import Blueprint, jsonify, request

from database.db import create_lead, get_leads


leads_bp = Blueprint("leads", __name__)


@leads_bp.post("/api/leads")
def create_lead_route():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        name = data.get("name", "")
        phone = data.get("phone", "")
        company = data.get("company", "")
        message = data.get("message", "")
        session_id = data.get("session_id", "")

        if not isinstance(name, str):
            return jsonify({
                "error": "Name must be a string."
            }), 400

        if not isinstance(phone, str):
            return jsonify({
                "error": "Phone must be a string."
            }), 400

        if not isinstance(company, str):
            return jsonify({
                "error": "Company must be a string."
            }), 400

        if not isinstance(message, str):
            return jsonify({
                "error": "Message must be a string."
            }), 400

        if not isinstance(session_id, str):
            return jsonify({
                "error": "Session ID must be a string."
            }), 400

        name = name.strip()
        phone = phone.strip()
        company = company.strip()
        message = message.strip()
        session_id = session_id.strip()

        if not name:
            return jsonify({
                "error": "Name is required."
            }), 400

        if not phone:
            return jsonify({
                "error": "Phone is required."
            }), 400

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
        print("LEAD ERROR:", repr(e))

        return jsonify({
            "error": "Lead could not be created.",
            "details": str(e)
        }), 500


@leads_bp.get("/api/leads")
def list_leads():
    try:
        leads = get_leads()

        return jsonify({
            "status": "success",
            "leads": leads
        }), 200

    except Exception as e:
        print("GET LEADS ERROR:", repr(e))

        return jsonify({
            "error": "Leads could not be retrieved.",
            "details": str(e)
        }), 500