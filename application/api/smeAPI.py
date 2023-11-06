import sqlalchemy.exc
from flask import Blueprint, request
from pydantic import BaseModel

from application import db, return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.Schema import validator
from application.models import School
from application.models.smeModel import SME
from application.utils.authenticator import authenticate, has_school_privilege
from exceptions.custom_exception import CustomException

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


@sme_bp.route("/<int:school_id>", methods=["POST"])
@authenticate(PermissionEnum.ADD_SME)
@has_school_privilege
def create_sme(school_id):
    sme_data = request.get_json()

    sme: SMESchema = validator.validate_data(SMESchema, sme_data)

    _school = School.GetSchool(school_id)

    try:
        sme_model = SME(
            name=sme.name,
            surname=sme.surname,
            email=sme.email,
            contact_telephone=sme.contact_telephone,
            website=sme.website,
            company_name=sme.company_name,
            registered_address=sme.registered_address,
            area_of_expertise=sme.area_of_expertise,
            nin_certificate=sme.nin_certificate,
            schools=_school
        )
        db.session.add(sme_model)
        db.session.commit()
        return return_json(OutputObj(code=201, message="SME created successfully"))

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        raise CustomException(message="An SME with that name or company_name already exist", status_code=400)
    except Exception as e:
        db.session.rollback()
        raise e


@sme_bp.route("/<int:school_id>", methods=["GET"])
@authenticate(PermissionEnum.VIEW_SME)
@has_school_privilege
def get_sme(school_id):
    sme = SME.query.filter_by(school_id=school_id).first()
    if not sme:
        raise CustomException(message="SME not found", status_code=404)
    return return_json(OutputObj(code=200, message="SME fetched", data=sme.to_dict(add_filter=False)))


@sme_bp.route("/<int:school_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_SME)
@has_school_privilege
def update_sme(school_id):
    _sme: SME = SME.query.filter_by(school_id=school_id).first()
    if not _sme:
        raise CustomException(message="SME not found", status_code=404)

    data = request.get_json()
    try:
        _sme.update_table(data)
        db.session.commit()
        return return_json(OutputObj(code=200, message="SME updated successfully"))

    except Exception as e:
        db.session.rollback()
        raise e


# Delete an SME by ID
@sme_bp.route("/<int:school_id>", methods=["DELETE"])
@authenticate(PermissionEnum.DELETE_SME)
@has_school_privilege
def delete_sme(school_id):
    sme = SME.query.filter_by(school_id=school_id).first()
    if not sme:
        raise CustomException(message="SME not found", status_code=404)

    db.session.delete(sme)
    db.session.commit()
    return return_json(OutputObj(code=200, message="SME deleted successfully"))
