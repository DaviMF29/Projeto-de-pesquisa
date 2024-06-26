from flask import request, jsonify, Blueprint

from controllers.user_controller import (
    create_user_controller,update_user_controller,delete_user_controller)

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


users_app = Blueprint("users_app", __name__)

allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com","aluno.uepb.edu.br"]

@users_app.route("/api/users", methods=["POST"])
def create_user_route():
    data = request.get_json()
    
    name = data["name"].lower()
    email = data["email"].lower()
    password = data["password"].lower()

    if len(password) < 6:
        return jsonify({"message": "Password must have at least 6 characters"}), 400

    if "@" not in email:
        return jsonify({"message": "Invalid email"}), 400

    domain = email.split("@")[-1]
    if domain not in allowed_domains:
        return jsonify({"message": "Only specific email domains are allowed"}), 401

    response, status_code = create_user_controller(email, name, password)
    return jsonify(response), status_code

@users_app.route("/api/users/<userId>", methods=["DELETE"])
@jwt_required()
def delete_user_route(userId):
    response, status_code = delete_user_controller(userId)
    return jsonify(response), status_code


@users_app.route("/api/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    data = request.get_json()

    try:
        update_user_controller(user_id, data)
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
