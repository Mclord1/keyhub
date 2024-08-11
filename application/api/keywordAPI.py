from flask import Blueprint, request

from application import return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.module.Keywords import KeywordModel
from application.utils.authenticator import authenticate

keywords_bp = Blueprint("keywords", __name__)


# Create a Keyword
@keywords_bp.route("/add", methods=["POST"])
@authenticate(PermissionEnum.ADD_KEYWORD)
def create_keyword():
    data = request.get_json()
    KeywordModel.create_keyword(data)
    return return_json(OutputObj(code=201, message="Keyword created successfully"))


@keywords_bp.route("/all", methods=["GET"])
@authenticate()
def get_all_keywords():
    keyword_list = KeywordModel.get_all_keywords()
    return return_json(OutputObj(code=200, message="keywords fetched", data=keyword_list))


# Update a Keyword by ID
@keywords_bp.route("/<int:keyword_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_KEYWORD)
def update_keyword(keyword_id):
    data = request.get_json()
    KeywordModel.update_keyword(keyword_id, data)
    return return_json(OutputObj(code=200, message="Keyword updated successfully"))


@keywords_bp.route("/<int:keyword_id>", methods=["DELETE"])
@authenticate(PermissionEnum.DEACTIVATE_KEYWORD)
def delete_keyword(keyword_id):
    KeywordModel.delete_keyword(keyword_id)
    return return_json(OutputObj(code=200, message="Keyword deleted successfully"))
