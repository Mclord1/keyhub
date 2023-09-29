from flask import Blueprint, request

from application.module.Students import StudentModel as Student
from application.utils.output import return_json, OutputObj
from . import *

student_blueprint = Blueprint('student', __name__)


@student_blueprint.route('/list-students', methods=['GET'])
@authenticate(PermissionEnum.VIEW_STUDENTS)
def list_students():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Students results", data=Student.get_all_students(page, per_page)))


@student_blueprint.route('/update-student', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def update_student():
    user_id = request.args.get('user_id', None)
    if not user_id:
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)
    args = request.json
    return return_json(OutputObj(code=200, message="Student information", data=Student.update_information(user_id, args)))


@student_blueprint.route('/add-student', methods=['POST'])
@authenticate(PermissionEnum.ADD_STUDENTS)
def add_student():
    req = request.json
    Student.add_student(req)
    return return_json(OutputObj(code=200, message="Student has been added successfully"))


@student_blueprint.route('/search-student', methods=['GET'])
@authenticate(PermissionEnum.VIEW_STUDENTS)
def search_student():
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Student results", data=Student.search_students(query)))


@student_blueprint.route('/reset-password', methods=['POST'])
@authenticate(PermissionEnum.RESET_STUDENT_PASSWORD)
def reset_password():
    req = request.json
    return return_json(OutputObj(code=200, message=Student.reset_password(req['user_id'])))


@student_blueprint.route('/delete-student', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_STUDENTS)
def delete_student():
    args = request.json
    student_id = args['student_id']
    reason = args['reason']
    return return_json(OutputObj(code=200, message="Student information", data=Student.deactivate_user(student_id, reason)))

