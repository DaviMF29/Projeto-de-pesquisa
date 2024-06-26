from models.User import User
import bcrypt
import base64
from flask import jsonify
from bson import ObjectId
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

def login(email, password):
    email = email.lower()
    user = User.get_user_by_email_model(email)
    if user and bcrypt.checkpw(password.encode(), base64.b64decode(user["password"])):
        access_token = create_access_token(identity=str(user["_id"]))
        return {"access_token": access_token}, 200
    else:
        return {"message": "Invalid email or password"}, 401

    
def get_user_data():
    user_id = get_jwt_identity()
    user_data = User.get_user_by_id_model(ObjectId(user_id))
    if user_data:
        user_data.pop('password', None)
        user_data['_id'] = str(user_data['_id'])
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404