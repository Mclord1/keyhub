from flask import Blueprint, request

from application.module.Admins import SystemAdmins
from application.utils.output import return_json, OutputObj
from . import *

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/add-admin', methods=['POST'])
@authenticate(PermissionEnum.ADD_SYSTEM_ADMIN)
def add_admin():
    req = request.json
    SystemAdmins.create_admin(req)
    return return_json(OutputObj(code=200, message="System Admin has been added successfully"))


@admin_blueprint.route('/reset-password', methods=['POST'])
@authenticate(PermissionEnum.RESET_SYSTEM_ADMIN_PASSWORD)
def reset_password():
    req = request.json
    return return_json(OutputObj(code=200, message=SystemAdmins.reset_password(req['user_id'])))


@admin_blueprint.route('/list-admin', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SYSTEM_ADMIN)
def list_admins():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Admin results", data=SystemAdmins.get_all_admin(page, per_page)))


@admin_blueprint.route('/update-admin', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_SYSTEM_ADMIN)
def update_admin():
    user_id = request.args.get('user_id', None)
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)
    args = request.json
    return return_json(OutputObj(code=200, message="User information has been updated successfully",
                                 data=SystemAdmins.update_admin(user_id, args)))


@admin_blueprint.route('/delete-admin', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_SYSTEM_ADMIN)
def delete_admin():
    args = request.json
    admin_id = args['admin_id']
    reason = args['reason']
    return return_json(
        OutputObj(code=200, message="Admin information", data=SystemAdmins.deactivate_user(admin_id, reason)))


@admin_blueprint.route('/search-admin', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SYSTEM_ADMIN)
def search_admin():
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Admin results", data=SystemAdmins.search_admin(query)))


@admin_blueprint.route('/get-admin/<int:id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SYSTEM_ADMIN)
def get_admin(id):
    return return_json(OutputObj(code=200, message="Admin results", data=SystemAdmins.get_user(id)))
