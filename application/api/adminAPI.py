from flask import Blueprint, request
from application.module.Admins import SystemAdmins
from . import *
from application.utils.output import return_json, OutputObj

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/add-admin', methods=['POST'])
@authenticate(PermissionEnum.CREATE_SYSTEM_ADMIN)
def add_admin():
    req = request.json
    SystemAdmins.CreateAdmin(req)
    return return_json(OutputObj(code=200, message="System Admin has been added successfully"))


@admin_blueprint.route('/reset-password', methods=['POST'])
@authenticate(PermissionEnum.RESET_PASSWORD)
def reset_password():
    req = request.json
    return return_json(OutputObj(code=200, message=SystemAdmins.ResetPassword(req['user_id'])))


@admin_blueprint.route('/list-admin', methods=['GET'])
@authenticate(PermissionEnum.RESET_PASSWORD)
def get_admins():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message=SystemAdmins.GetAllAdmin(page, per_page)))
