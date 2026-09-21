import secrets

from flask import Blueprint, jsonify, request

from app import db
from app.models import Category, Ticket, User


api = Blueprint("api", __name__, url_prefix="/api")


def get_api_user():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header[7:].strip()

    if not token:
        return None

    return User.query.filter_by(api_token=token).first()


@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


@api.route("/token", methods=["POST"])
def token():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON-Daten fehlen."
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "error": "Benutzername und Passwort sind erforderlich."
        }), 400

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({
            "error": "Ungültige Zugangsdaten."
        }), 401

    if not user.api_token:
        user.api_token = secrets.token_hex(32)
        db.session.commit()

    return jsonify({
        "token": user.api_token,
        "token_type": "Bearer"
    })


@api.route("/tickets", methods=["GET"])
def tickets():
    user = get_api_user()

    if user is None:
        return jsonify({
            "error": "Bearer Token fehlt oder ist ungültig."
        }), 401

    user_tickets = Ticket.query.filter_by(
        user_id=user.id
    ).order_by(Ticket.created_at.desc()).all()

    result = []

    for ticket in user_tickets:
        result.append({
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "category": {
                "id": ticket.category.id,
                "name": ticket.category.name
            },
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat()
        })

    return jsonify(result)


@api.route("/tickets/<int:ticket_id>", methods=["GET"])
def ticket_detail(ticket_id):
    user = get_api_user()

    if user is None:
        return jsonify({
            "error": "Bearer Token fehlt oder ist ungültig."
        }), 401

    ticket = Ticket.query.filter_by(
        id=ticket_id,
        user_id=user.id
    ).first()

    if ticket is None:
        return jsonify({
            "error": "Ticket nicht gefunden."
        }), 404

    return jsonify({
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "category": {
            "id": ticket.category.id,
            "name": ticket.category.name
        },
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat()
    })


@api.route("/categories", methods=["GET"])
def categories():
    user = get_api_user()

    if user is None:
        return jsonify({
            "error": "Bearer Token fehlt oder ist ungültig."
        }), 401

    categories = Category.query.order_by(Category.name).all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }
        for category in categories
    ])
