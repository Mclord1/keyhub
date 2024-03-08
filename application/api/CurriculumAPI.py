from flask import Blueprint, request

from application import return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.module.Curriculum import CurriculumModel
from application.utils.authenticator import authenticate

curriculum_bp = Blueprint("curriculums", __name__)


@curriculum_bp.route("/add", methods=["POST"])
@authenticate(PermissionEnum.ADD_KEYWORD)
def create_curriculum():
    data = request.get_json()
    CurriculumModel.create_curriculum(data)
    return return_json(OutputObj(code=201, message="Curriculum created successfully"))


@curriculum_bp.route("/all", methods=["GET"])
@authenticate()
def get_all_curriculum():
    curriculum_list = CurriculumModel.get_all_curriculum()
    return return_json(OutputObj(code=200, message="Curriculums fetched", data=curriculum_list))


@curriculum_bp.route("/<int:curriculum_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_KEYWORD)
def update_curriculum(curriculum_id):
    data = request.get_json()
    CurriculumModel.update_curriculum(curriculum_id, data)
    return return_json(OutputObj(code=200, message="Curriculum updated successfully"))


@curriculum_bp.route("/<int:curriculum_id>", methods=["DELETE"])
@authenticate(PermissionEnum.DEACTIVATE_KEYWORD)
def delete_curriculum(curriculum_id):
    CurriculumModel.delete_curriculum(curriculum_id)
    return return_json(OutputObj(code=200, message="Curriculum deleted successfully"))
