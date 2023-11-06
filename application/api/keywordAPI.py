import sqlalchemy.exc
from flask import Blueprint, request

from application import db, return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.models.smeModel import Keywords
from application.utils.authenticator import authenticate
from exceptions.custom_exception import CustomException

keywords_bp = Blueprint("keywords", __name__)


# Create a Keyword
@keywords_bp.route("/add", methods=["POST"])
@authenticate(PermissionEnum.ADD_KEYWORD)
def create_keyword():
    data = request.get_json()
    if "name" not in data:
        raise CustomException(message="name is required", status_code=400)

    try:
        keyword = Keywords(**data)
        keyword.save(refresh=True)
        return return_json(OutputObj(code=201, message="Keyword created successfully"))

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        raise CustomException(message="A keyword with that name already exist", status_code=400)
    except Exception as e:
        db.session.rollback()
        raise e


@keywords_bp.route("/all", methods=["GET"])
@authenticate(PermissionEnum.VIEW_KEYWORD)
def get_all_keywords():
    keywords = Keywords.query.all()
    keyword_list = [keyword.to_dict(add_filter=False) for keyword in keywords]
    return return_json(OutputObj(code=200, message="keywords fetched", data=keyword_list))


# Update a Keyword by ID
@keywords_bp.route("/<int:keyword_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_KEYWORD)
def update_keyword(keyword_id):
    keyword = Keywords.query.filter_by(id=keyword_id).first()
    if not keyword:
        raise CustomException(message="Keyword not found", status_code=404)

    data = request.get_json()
    if "name" not in data:
        raise CustomException(message="name is required", status_code=400)

    try:
        keyword.update_table(data)
        db.session.commit()
        return return_json(OutputObj(code=200, message="Keyword updated successfully"))

    except Exception as e:
        db.session.rollback()
        raise e


@keywords_bp.route("/<int:keyword_id>", methods=["DELETE"])
@authenticate(PermissionEnum.DEACTIVATE_KEYWORD)
def delete_keyword(keyword_id):
    keyword = Keywords.query.filter_by(id=keyword_id).first()
    if not keyword:
        raise CustomException(message="Keyword not found", status_code=404)

    db.session.delete(keyword)
    db.session.commit()
    return return_json(OutputObj(code=200, message="Keyword deleted successfully"))
