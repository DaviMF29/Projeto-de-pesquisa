from flask import abort
from models.Student import Student
from models.User import User

def verify_user(userId):
    user = User.get_user_by_id_model(userId)
    if not user:
        abort(400, {"message": "User not exist"})
    return user

def verify_student(studentId):
    student = Student.get_student_by_id_model(studentId)
    if not student:
        abort(400, {"message": "Student not exist"})
    return student

def verify_username_registered(username):
    user = User.get_user_by_username_model(username)
    if user:
        abort(400, {"message": "Username is not available"})
    return {"message": "Username is available"}

def verify_email_registered(email):          
    user = User.get_user_by_email_model(email)
    if user:
        abort(400, {"message": "Email is not available"})
    return {"message": "Email is available"}
 
def verify_change_in_user(user_id, field_name, new_value):
    user = verify_user(user_id)
    if field_name in user:
        current_value = user[field_name]
        if current_value == new_value:
            abort(400, f"The {field_name} is the same")
        return current_value
    else:
        abort(400, f"User data is missing '{field_name}' field")