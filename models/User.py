from pymongo import MongoClient
from bson import ObjectId
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db_name = "redesocial"
db = client[db_name]


class User:

    @staticmethod
    def create_user_model(name, email, new_pass_base64, birth=None, gender=None,
                           period=None, registration=None, city=None, state=None, institution=None):
        users_collection = db.users
        new_user = {
            "nome": name,
            "email": email,
            "nascimento": birth,
            "gender": gender,
            "period": period,
            "registration": registration,
            "password": new_pass_base64,
            "city": city,
            "state": state,
            "institution": institution,
        }
        result = users_collection.insert_one(new_user)
        return str(result.inserted_id)

    
    @staticmethod
    def get_user_by_email_model(email):
        users_collection = db.users
        user = users_collection.find_one({"email": email})
        return user
    
    @staticmethod
    def get_user_by_id_model(id):
        users_collection = db.users
        user = users_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None
    
    @staticmethod
    def update_user(user_id, updated_fields):
        users_collection = db.users
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_fields})
        return result
        
    @staticmethod
    def delete_account_model(user_id):
        users_collection = db.users
        result = users_collection.find_one_and_delete({"_id": ObjectId(user_id)})
        return result
    
    def add_new_field_to_all_users(new_field_name):
        users_collection = db.users
        result = users_collection.update_many({}, {"$set": {new_field_name: []}})
        return result

    
    def update_user_image_model(user_id, image_url):
        users_collection = db.users
        result = users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'image': image_url}}
        )

        if result.modified_count == 0:
            raise Exception(f"Failed to update user's image with id {user_id}.")

        return {"message": "Image added successfully"}