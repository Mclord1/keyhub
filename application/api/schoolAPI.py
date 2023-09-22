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


@school_blueprint.route('/<int:id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
def update_school_info(id):
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolModel.update_school(id, req)))


@school_blueprint.route('/<int:id>/toggle-status', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_SCHOOL)
def toggle_status(id):
    req = request.json.get('status')
    if not isinstance(req, bool):
        raise CustomException(message="Argument 'status' must be provided and is boolean")
    return return_json(OutputObj(code=200, message=SchoolModel.toggle_status(id, req)))


@school_blueprint.route('/list', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL)
def list_school():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school information", data=SchoolModel.list_all_schools(page, per_page)))


@school_blueprint.route('/<int:id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL)
def view_school_info(id):
    return return_json(OutputObj(code=200, message="school results", data=SchoolModel.view_school_info(id)))


@school_blueprint.route('/<int:id>/school-admins', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL_MANAGERS)
def school_managers_list(id):
    return return_json(OutputObj(code=200, message="school Admins results", data=SchoolModel.get_account_admins(id)))


@school_blueprint.route('/<int:id>/parents', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PARENTS)
def school_parents_list(id):
    return return_json(OutputObj(code=200, message="school parents results", data=SchoolModel.get_parents(id)))


@school_blueprint.route('/<int:id>/students', methods=['GET'])
@authenticate(PermissionEnum.VIEW_STUDENTS)
def school_students_list(id):
    return return_json(OutputObj(code=200, message="school students results", data=SchoolModel.get_students(id)))


@school_blueprint.route('/<int:id>/teachers', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TEACHERS)
def school_teachers_list(id):
    return return_json(OutputObj(code=200, message="school teachers results", data=SchoolModel.get_teachers(id)))


@school_blueprint.route('/<int:id>/projects', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PROJECTS)
def school_projects_list(id):
    return return_json(OutputObj(code=200, message="school projects results", data=SchoolModel.get_projects(id)))
