from flask import request, jsonify, Blueprint
from controllers.auth_controller import login
from flask_jwt_extended import jwt_required
from controllers.auth_controller import get_user_data
auth_app = Blueprint("auth_app", __name__)


@auth_app.route("/api/login", methods=["POST"])
def login_route():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        return jsonify({"error": "A field is missing"}), 400
    email = data["email"]
    password = data["password"]

    response, status_code = login(email, password)
    return jsonify(response), 200 if status_code == 200 else 401

@auth_app.route('/api/data_user', methods=['GET'])
@jwt_required()
def get_user_data_route():
    return get_user_data()