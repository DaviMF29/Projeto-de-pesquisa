import base64
import uuid
import bcrypt
from bson import ObjectId
from db.firebase import *
from models.User import User


from middleware.global_middleware import (
    verify_email_registered,verify_user,verify_change_in_user,
    )


def create_user_controller(email,username, password):
    verify_email_registered(email)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))
    hashed_password_base64 = base64.b64encode(hashed_password).decode()
    image = ""
    user_id = User.create_user_model(username,email,image, hashed_password_base64)
    return {"id": user_id, "message": f"User {username} created"}, 201

def update_user_controller(user_id, new_data):
    updated_fields = {}
    for key, value in new_data.items():
        if key != "_id":  # proibir alteração do _id
            updated_fields[key] = value

    for field_name, new_value in updated_fields.items():
        verify_change_in_user(user_id, field_name, new_value)

    User.update_user(user_id, updated_fields)

    return {"message": "User updated"}, 200

def delete_user_controller(userId):
    verify_user(userId)
    User.delete_account_model(userId)
    return {"message": "User deleted"}, 200

def get_user_by_id_controller(user_id):
    try:
        user_id = ObjectId(user_id)
        user = User.get_user_by_id_model(user_id)
        if not user:
            return {"message": "User not found"}, 404

        user.pop('_id', None)

        return user
    except Exception as e:
        print(f"Failed to retrieve user: {e}")
        return {"message": "Failed to retrieve user"}, 500
