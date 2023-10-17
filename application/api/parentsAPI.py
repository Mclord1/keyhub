from flask import Blueprint, request

from application.module.Parents import ParentModel as Parent
from application.utils.output import return_json, OutputObj
from . import *

parent_blueprint = Blueprint('parent', __name__)


@parent_blueprint.route('/list-parents', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PARENTS)
def list_parents():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Parents results", data=Parent.get_all_parents(page, per_page)))


@parent_blueprint.route('/update-parent', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_PARENTS)
def update_parent():
    user_id = request.args.get('user_id', None)
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)
    args = request.json
    return return_json(OutputObj(code=200, message="Parent information", data=Parent.update_information(user_id, args)))


@parent_blueprint.route('/add-parent', methods=['POST'])
@authenticate(PermissionEnum.ADD_PARENTS)
def add_parent():
    req = request.json
    Parent.add_parent(req)
    return return_json(OutputObj(code=200, message="Parent has been added successfully"))


@parent_blueprint.route('/search-parent', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PARENTS)
def search_parent():
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Parent results", data=Parent.search_parents(query)))


@parent_blueprint.route('/reset-password', methods=['POST'])
@authenticate(PermissionEnum.RESET_PARENTS_PASSWORD)
def reset_password():
    req = request.json
    return return_json(OutputObj(code=200, message=Parent.reset_password(req['user_id'])))


@parent_blueprint.route('/delete-parent', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_PARENTS)
def delete_parent():
    args = request.json
    parent_id = args['parent_id']
    reason = args['reason']
    return return_json(
        OutputObj(code=200, message="Parent information", data=Parent.deactivate_user(parent_id, reason)))


@parent_blueprint.route('/get-parent/<int:id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PARENTS)
def get_parent(id):
    return return_json(OutputObj(code=200, message="Parent results", data=Parent.get_user(id)))
