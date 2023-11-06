from flask import Blueprint, request

from application import return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.module.Sme import SmeModel
from application.utils.authenticator import authenticate, has_school_privilege

sme_bp = Blueprint("sme", __name__)


@sme_bp.route("/<int:school_id>", methods=["POST"])
@authenticate(PermissionEnum.ADD_SME)
@has_school_privilege
def create_sme(school_id):
    sme_data = request.get_json()
    SmeModel.create_sme(school_id, sme_data)
    return return_json(OutputObj(code=201, message="SME created successfully"))


@sme_bp.route("/<int:school_id>", methods=["GET"])
@authenticate(PermissionEnum.VIEW_SME)
@has_school_privilege
def get_sme(school_id):
    sme = SmeModel.get_sme(school_id)
    return return_json(OutputObj(code=200, message="SME fetched", data=sme))


@sme_bp.route("/<int:school_id>/all", methods=["GET"])
@authenticate(PermissionEnum.VIEW_SME)
@has_school_privilege
def get_all_sme(school_id):
    sme = SmeModel.get_all_sme(school_id)
    return return_json(OutputObj(code=200, message="SME fetched", data=sme))


@sme_bp.route("/<int:school_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_SME)
@has_school_privilege
def update_sme(school_id):
    data = request.get_json()
    SmeModel.update_sme(school_id, data)
    return return_json(OutputObj(code=200, message="SME updated successfully"))


# Delete an SME by ID
@sme_bp.route("/<int:school_id>", methods=["DELETE"])
@authenticate(PermissionEnum.DELETE_SME)
@has_school_privilege
def delete_sme(school_id):
    SmeModel.delete_sme(school_id)
    return return_json(OutputObj(code=200, message="SME deleted successfully"))
