import base64
import bcrypt
from bson import ObjectId
from db.firebase import *
from models.Student import Student


from middleware.global_middleware import (
    verify_email_registered,verify_student
    )


def create_student_controller(email,studentname, password):
    verify_email_registered(email)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))
    hashed_password_base64 = base64.b64encode(hashed_password).decode()
    image = ""
    student_id = Student.create_student_model(studentname,email,image, hashed_password_base64)
    return {"id": student_id, "message": f"student {studentname} created"}, 201


def delete_student_controller(studentId):
    verify_student(studentId)
    Student.delete_account_model(studentId)
    return {"message": "student deleted"}, 200

def get_student_by_id_controller(student_id):
    try:
        student_id = ObjectId(student_id)
        student = Student.get_student_by_id_model(student_id)
        if not student:
            return {"message": "student not found"}, 404

        student.pop('_id', None)

        return student
    except Exception as e:
        print(f"Failed to retrieve student: {e}")
        return {"message": "Failed to retrieve student"}, 500

