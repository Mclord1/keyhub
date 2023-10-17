from flask import Blueprint, request

from application.module.Schools import SchoolModel
from application.utils.output import return_json, OutputObj
from . import *

school_blueprint = Blueprint('school', __name__)


@school_blueprint.route('/add-school', methods=['POST'])
@authenticate(PermissionEnum.ADD_SCHOOL)
def add_school():
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolModel.add_school(req)))


@school_blueprint.route('/<int:school_id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def update_school_info(school_id):
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolModel.update_school(school_id, req)))


@school_blueprint.route('/<int:school_id>/toggle-status', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_SCHOOL)
@has_school_privilege
def toggle_status(school_id):
    req = request.json.get('status')
    if not isinstance(req, bool):
        raise CustomException(message="Argument 'status' must be provided and is boolean")
    return return_json(OutputObj(code=200, message=SchoolModel.toggle_status(school_id, req)))


@school_blueprint.route('/list', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL)
def list_school():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="school information", data=SchoolModel.list_all_schools(page, per_page)))


@school_blueprint.route('/<int:school_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL)
@has_school_privilege
def view_school_info(school_id):
    return return_json(OutputObj(code=200, message="school results", data=SchoolModel.view_school_info(school_id)))


@school_blueprint.route('/<int:school_id>/school-admins', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL_MANAGERS)
@has_school_privilege
def school_managers_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="school Admins results", data=SchoolModel.get_account_admins(school_id, page,per_page)))


@school_blueprint.route('/<int:school_id>/parents', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PARENTS)
@has_school_privilege
def school_parents_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school parents results", data=SchoolModel.get_parents(school_id, page,per_page)))


@school_blueprint.route('/<int:school_id>/students', methods=['GET'])
@authenticate(PermissionEnum.VIEW_STUDENTS)
@has_school_privilege
def school_students_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school students results", data=SchoolModel.get_students(school_id,page,per_page)))


@school_blueprint.route('/<int:school_id>/teachers', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TEACHERS)
@has_school_privilege
def school_teachers_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school teachers results", data=SchoolModel.get_teachers(school_id, page,per_page)))


@school_blueprint.route('/<int:school_id>/projects', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PROJECTS)
@has_school_privilege
def school_projects_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school projects results",
                                 data=SchoolModel.get_projects(school_id, page, per_page)))
