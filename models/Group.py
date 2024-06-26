from pymongo import MongoClient
from bson import ObjectId
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db_name = "redesocial"
db = client[db_name]


class Group:

    @staticmethod
    def create_group_model(name, period, students = []):
        groups_collection = db.groups
        new_group = {
            "nome": name,
            "period": period,
            "students": students
        }
        result = groups_collection.insert_one(new_group)
        return str(result.inserted_id)
    
    @staticmethod
    def delete_student_from_group_model(group_id, student_id):
        groups_collection = db.groups
        groups_collection.update_one({"_id": ObjectId(group_id)}, {"$pull": {"students": student_id}})

    @staticmethod
    def add_student_to_group_model(group_id, student_id):
        groups_collection = db.groups
        groups_collection.update_one({"_id": ObjectId(group_id)}, {"$push": {"students": student_id}})

    @staticmethod
    def get_students_from_group_model(group_id):
        groups_collection = db.groups
        group = groups_collection.find_one({"_id": ObjectId(group_id)})
        return group["students"]