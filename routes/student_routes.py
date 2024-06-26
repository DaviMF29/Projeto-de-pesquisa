from flask import request, jsonify, Blueprint

from controllers.student_controller import (
    create_student_controller,delete_student_controller)

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


student_app = Blueprint("student_app", __name__)

allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com","aluno.uepb.edu.br"]

@student_app.route("/api/students", methods=["POST"])
def create_student_route():
    data = request.get_json()
    
    studentname = data["studentname"].lower()
    email = data["email"].lower()
    password = data["password"].lower()

    if len(password) < 6:
        return jsonify({"message": "Password must have at least 6 characters"}), 400

    if "@" not in email:
        return jsonify({"message": "Invalid email"}), 400

    domain = email.split("@")[-1]
    if domain not in allowed_domains:
        return jsonify({"message": "Only specific email domains are allowed"}), 401

    response, status_code = create_student_controller(email, studentname, password)
    return jsonify(response), status_code

@student_app.route("/api/students/<studentId>", methods=["DELETE"])
@jwt_required()
def delete_student_route(studentId):
    response, status_code = delete_student_controller(studentId)
    return jsonify(response), status_code

