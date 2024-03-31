from flask import Blueprint, request

from application.module.Students import StudentModel as Student
from application.utils.output import return_json, OutputObj
from . import *
from ..Enums.Permission import SchoolPermissionEnum

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
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass a correct user id as query parameter", status_code=400)
    args = request.json
    return return_json(OutputObj(code=200, message="Student information", data=Student.update_information(user_id, args)))


@student_blueprint.route('/add-student', methods=['POST'])
def add_student():
    req = request.json
    Student.add_student(req)
    return return_json(OutputObj(code=200, message="Student has been added successfully"))


@student_blueprint.route('/search-student', methods=['GET'])
@authenticate(PermissionEnum.VIEW_STUDENTS)
def search_student():
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Student results", data=Student.search_students(query)))


@student_blueprint.route('/remove-parent', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def remove_parent():
    req = request.json
    student_id = req.get('student_id')
    parent_id = req.get('parent_id')
    return return_json(OutputObj(code=200, message=Student.remove_parent(student_id, parent_id)))


@student_blueprint.route('/add-parent', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def add_parent():
    req = request.json
    student_id = req.get('student_id')
    parent_id = req.get('parent_id')
    return return_json(OutputObj(code=200, message=Student.add_parent(student_id, parent_id)))


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


@student_blueprint.route('/change-profile-image', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def update_student_profile_image():
    user_id = request.args.get('user_id', None)
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)

    args = request.json
    profile_image = args.get("profile_image", None)
    return return_json(OutputObj(code=200, message="", data=Student.change_student_profile_image(profile_image, user_id)))


@student_blueprint.route('/get-student/<int:id>', methods=['GET'])
@authenticate([PermissionEnum.VIEW_STUDENTS, SchoolPermissionEnum.VIEW_STUDENTS])
def get_student(id):
    return return_json(OutputObj(code=200, message="Student results", data=Student.get_user(id)))


@student_blueprint.route('/<int:id>/comment', methods=['POST'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def add_student_comment(id):
    data = request.json
    comment = data.get('comment')
    if not comment:
        raise CustomException(message="Please provide comment", status_code=400)
    return return_json(OutputObj(code=200, message=Student.add_comment(id, comment)))


@student_blueprint.route('/<int:id>/comment', methods=['GET'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def get_student_comment(id):
    return return_json(OutputObj(code=200, message="comment fetched", data=Student.get_comments(id)))


@student_blueprint.route('/<int:id>/comment/<int:comment_id>', methods=['DELETE'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def remove_student_comment(id, comment_id):
    return return_json(OutputObj(code=200, message=Student.remove_comment(id, comment_id)))


@student_blueprint.route('/<int:id>/comment/<int:comment_id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def edit_student_comment(id, comment_id):
    data = request.json
    comment = data.get('comment')
    if not comment:
        raise CustomException(message="Please provide comment", status_code=400)
    return return_json(OutputObj(code=200, message=Student.edit_comments(id, comment_id, comment)))


@student_blueprint.route('/<int:id>/file', methods=['POST'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def add_student_file(id):
    data = request.json
    file = data.get('file')
    file_name = data.get('file_name')
    if not file:
        raise CustomException(message="Please provide file", status_code=400)
    if not file_name:
        raise CustomException(message="Please provide file_name", status_code=400)
    return return_json(OutputObj(code=200, message=Student.add_file(id, file, file_name)))


@student_blueprint.route('/<int:id>/file', methods=['GET'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def get_student_file(id):
    return return_json(OutputObj(code=200, message="file fetched", data=Student.get_files(id)))


@student_blueprint.route('/<int:id>/file/<int:file_id>', methods=['DELETE'])
@authenticate(PermissionEnum.MODIFY_STUDENTS)
def remove_student_file(id, file_id):
    return return_json(OutputObj(code=200, message=Student.remove_file(id, file_id)))
