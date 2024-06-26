from pymongo import MongoClient
from bson import ObjectId
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db_name = "redesocial"
db = client[db_name]


class Student:

    @staticmethod
    def create_student_model(name, email, new_pass_base64, birth=None, gender=None,
                           period=None, registration=None, city=None, state=None, institution=None):
        student_collection = db.students
        new_student = {
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
        result = student_collection.insert_one(new_student)
        return str(result.inserted_id)

    
    @staticmethod
    def get_student_by_email_model(email):
        students_collection = db.students
        student = students_collection.find_one({"email": email})
        return student
    
    @staticmethod
    def get_student_by_id_model(id):
        students_collection = db.students
        student = students_collection.find_one({"_id": ObjectId(id)})
        if student:
            student["_id"] = str(student["_id"])
            return student
        return None
    
    @staticmethod
    def update_student(student_id, updated_fields):
        students_collection = db.students
        result = students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_fields})
        return result
        
    @staticmethod
    def delete_account_model(student_id):
        students_collection = db.students
        result = students_collection.find_one_and_delete({"_id": ObjectId(student_id)})
        return result
    
    def add_new_field_to_all_students(new_field_name):
        students_collection = db.students
        result = students_collection.update_many({}, {"$set": {new_field_name: []}})
        return result

    
    def update_student_image_model(student_id, image_url):
        students_collection = db.students
        result = students_collection.update_one(
            {'_id': ObjectId(student_id)},
            {'$set': {'image': image_url}}
        )

        if result.modified_count == 0:
            raise Exception(f"Failed to update student's image with id {student_id}.")

        return {"message": "Image added successfully"}