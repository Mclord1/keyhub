from flask import Blueprint, request

from application.module.Teachers import TeacherModel as Teacher
from application.utils.output import return_json, OutputObj
from . import *
from ..Enums.Permission import SchoolPermissionEnum

teacher_blueprint = Blueprint('teacher', __name__)


@teacher_blueprint.route('/list-teachers', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TEACHERS)
def list_teachers():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Teachers results", data=Teacher.get_all_teachers(page, per_page)))


@teacher_blueprint.route('/update-teacher', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_TEACHER)
def update_teacher():
    user_id = request.args.get('user_id', None)
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)
    args = request.json
    return return_json(
        OutputObj(code=200, message="Teacher information", data=Teacher.update_information(user_id, args)))


@teacher_blueprint.route('/add-teacher', methods=['POST'])
def add_teacher():
    req = request.json
    Teacher.add_teacher(req)
    return return_json(OutputObj(code=200, message="Teacher has been added successfully"))


@teacher_blueprint.route('/search-teacher', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TEACHERS)
def search_teacher():
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Teacher results", data=Teacher.search_teachers(query)))


@teacher_blueprint.route('/change-profile-image', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_TEACHER)
def update_teacher_profile_image():
    user_id = request.args.get('user_id', None)
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)

    args = request.json
    profile_image = args.get("profile_image", None)
    return return_json(OutputObj(code=200, message="", data=Teacher.change_teacher_profile_image(profile_image, user_id)))



@teacher_blueprint.route('/reset-password', methods=['POST'])
@authenticate(PermissionEnum.RESET_TEACHER_PASSWORD)
def reset_password():
    req = request.json
    return return_json(OutputObj(code=200, message=Teacher.reset_password(req['user_id'])))


@teacher_blueprint.route('/delete-teacher', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_TEACHER)
def delete_teacher():
    args = request.json
    teacher_id = args['teacher_id']
    reason = args['reason']
    return return_json(
        OutputObj(code=200, message="Teacher information", data=Teacher.deactivate_user(teacher_id, reason)))


@teacher_blueprint.route('/get-teacher/<int:id>', methods=['GET'])
@authenticate([PermissionEnum.VIEW_TEACHERS, SchoolPermissionEnum.VIEW_TEACHERS])
def get_teacher(id):
    return return_json(OutputObj(code=200, message="Student results", data=Teacher.get_user(id)))
