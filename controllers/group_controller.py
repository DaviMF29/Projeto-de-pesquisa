import base64
import bcrypt
from bson import ObjectId
from db.firebase import *
from models.Group import Group


from middleware.global_middleware import (
    verify_email_registered,verify_user
    )



def create_group_controller(name, period):
    group_id = Group.create_group_model(name, period)
    return {"id": group_id, "message": f"Group {name} created"}, 201

def delete_student_from_group_controller(group_id, student_id):
    Group.delete_student_from_group_model(group_id, student_id)
    return {"message": "Student deleted from group"}, 200

def add_student_to_group_controller(group_id, student_id):
    Group.add_student_to_group_model(group_id, student_id)
    return {"message": "Student added to group"}, 200

def get_students_from_group_controller(group_id):
    students = Group.get_students_from_group_model(group_id)
    return {"students": students}, 200