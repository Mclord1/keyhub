from flask import Blueprint, request

from application.module.Schools import SchoolModel
from application.utils.output import return_json, OutputObj
from . import *

school_blueprint = Blueprint('school', __name__)


@admin_blueprint.route('/add-school', methods=['POST'])
@authenticate(PermissionEnum.ADD_SCHOOL)
def add_school():
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolModel.add_school(req)))


@admin_blueprint.route('/list', methods=['GET'])
@authenticate(PermissionEnum.LIST_SCHOOL)
def list_school():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school information", data=SchoolModel.list_all_schools(page, per_page)))


@admin_blueprint.route('/<int:id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_ADMIN)
def view_school_info(id):
    return return_json(OutputObj(code=200, message="school results", data=SchoolModel.view_school_info(id)))
