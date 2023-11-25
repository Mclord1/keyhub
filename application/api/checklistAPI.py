from flask import Blueprint, request

from application import return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.module.Checklists import CheckListModel
from application.utils.authenticator import authenticate

checklists_bp = Blueprint("checklist", __name__)


# Create a checklist
@checklists_bp.route("/add", methods=["POST"])
@authenticate(PermissionEnum.ADD_CHECKLIST)
def create_checklist():
    data = request.get_json()
    CheckListModel.create_checklist(data)
    return return_json(OutputObj(code=201, message="checklist created successfully"))


@checklists_bp.route("/all", methods=["GET"])
@authenticate(PermissionEnum.VIEW_CHECKLIST)
def get_all_checklists():
    checklist_list = CheckListModel.get_all_checklist()
    return return_json(OutputObj(code=200, message="checklists fetched", data=checklist_list))


# Update a checklist by ID
@checklists_bp.route("/<int:checklist_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_CHECKLIST)
def update_checklist(checklist_id):
    data = request.get_json()
    CheckListModel.update_checklist(checklist_id, data)
    return return_json(OutputObj(code=200, message="checklist updated successfully"))


@checklists_bp.route("/<int:checklist_id>", methods=["DELETE"])
@authenticate(PermissionEnum.DELETE_CHECKLIST)
def delete_checklist(checklist_id):
    CheckListModel.delete_checklist(checklist_id)
    return return_json(OutputObj(code=200, message="checklist deleted successfully"))
