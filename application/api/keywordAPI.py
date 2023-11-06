from flask import Blueprint, request, jsonify

from application import db
from application.Enums.Permission import PermissionEnum
from application.models.smeModel import Keywords
from application.utils.authenticator import authenticate

keywords_bp = Blueprint("keywords", __name__)


# Create a Keyword
@keywords_bp.route("/add", methods=["POST"])
@authenticate(PermissionEnum.ADD_SCHOOL)
def create_keyword():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "name is required"}), 400

    keyword = Keywords(**data)
    db.session.add(keyword)
    db.session.commit()
    return jsonify({"message": "Keyword created successfully"}), 201


# Get all Keywords
@keywords_bp.route("/all", methods=["GET"])
@authenticate(PermissionEnum.ADD_SCHOOL)
def get_all_keywords():
    keywords = Keywords.query.all()
    keyword_list = [keyword.serialize() for keyword in keywords]
    return jsonify(keyword_list)


# Update a Keyword by ID
@keywords_bp.route("/<int:keyword_id>", methods=["PUT"])
@authenticate(PermissionEnum.ADD_SCHOOL)
def update_keyword(keyword_id):
    keyword = Keywords.query.filter(Keywords.id == keyword_id).first()
    if not keyword:
        return jsonify({"error": "Keyword not found"}), 404

    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "name is required"}), 400

    keyword.update(**data)
    db.session.commit()
    return jsonify({"message": "Keyword updated successfully"})


# Delete a Keyword by ID
@keywords_bp.route("/<int:keyword_id>", methods=["DELETE"])
@authenticate(PermissionEnum.ADD_SCHOOL)
def delete_keyword(keyword_id):
    keyword = Keywords.query.filter(Keywords.id == keyword_id).first()
    if not keyword:
        return jsonify({"error": "Keyword not found"}), 404

    db.session.delete(keyword)
    db.session.commit()
    return jsonify({"message": "Keyword deleted successfully"})
