from flask import Blueprint, request

from application.module.Teachers import Teacher
from application.utils.output import return_json, OutputObj
from . import *

teacher_blueprint = Blueprint('teacher', __name__)


@teacher_blueprint.route('/list-teachers', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TEACHERS)
def list_teachers():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Teachers results", data=Teacher.get_all_teachers(page, per_page)))


@admin_blueprint.route('/update-teacher', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_TEACHER)
def update_teacher():
    user_id = request.args.get('user_id', None)
    if not user_id:
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)
    args = request.json
    return return_json(OutputObj(code=200, message="Admin information", data=Teacher.update_information(user_id, args)))

