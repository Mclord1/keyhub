from flask import Blueprint, request, jsonify
from pydantic import BaseModel

from application import db
from application.Enums.Permission import PermissionEnum
from application.Schema import validator
from application.models.smeModel import SME
from application.utils.authenticator import authenticate, has_school_privilege

sme_bp = Blueprint("sme", __name__)


class SMESchema(BaseModel):
    name: str
    surname: str
    email: str
    contact_telephone: str
    website: str
    company_name: str
    registered_address: str
    area_of_expertise: str
    nin_certificate: bool


class KeywordSchema(BaseModel):
    name: str


# Create an SME
@sme_bp.route("/<int:school_id>", methods=["POST"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def create_sme(school_id):
    sme_data = request.get_json()
    sme_data['school_id'] = school_id

    sme = validator.validate_data(SMESchema, sme_data)
    sme_model = SME(**sme.model_dump())
    db.session.add(sme_model)
    db.session.commit()
    return jsonify({"message": "SME created successfully"}), 201


@sme_bp.route("/<int:school_id>", methods=["GET"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def get_sme(school_id):
    sme = SME.query.fiilter(SME.school_id == school_id).first()
    if not sme:
        return jsonify({"error": "SME not found"}), 404
    return jsonify(sme.serialize())


# Update an SME by ID
@sme_bp.route("/<int:school_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def update_sme(school_id):
    sme = SME.query.fiilter(SME.school_id == school_id).first()
    if not sme:
        return jsonify({"error": "SME not found"}), 404

    data = request.get_json()
    sme.update(**data)
    db.session.commit()
    return jsonify({"message": "SME updated successfully"})


# Delete an SME by ID
@sme_bp.route("/<int:school_id>", methods=["DELETE"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def delete_sme(school_id):
    sme = SME.query.fiilter(SME.school_id == school_id).first()
    if not sme:
        return jsonify({"error": "SME not found"}), 404

    db.session.delete(sme)
    db.session.commit()
    return jsonify({"message": "SME deleted successfully"})
