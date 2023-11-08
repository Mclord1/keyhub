from . import *


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


class SmeModel:
    @classmethod
    def create_sme(cls, school_id, sme_data):
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
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="An SME with that name or company_name already exists", status_code=400)
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_sme(cls, school_id):
        sme = SME.query.filter_by(school_id=school_id).first()
        if not sme:
            raise CustomException(message="SME not found", status_code=404)
        return sme.to_dict(add_filter=False)

    @classmethod
    def get_all_sme(cls, school_id):
        sme = SME.query.filter_by(school_id=school_id).all()
        return [x.to_dict(add_filter=False) for x in sme]

    @classmethod
    def update_sme(cls, school_id, sme_id, data):
        _sme = SME.query.filter_by(school_id=school_id, id=sme_id).first()
        if not _sme:
            raise CustomException(message="SME not found", status_code=404)

        try:
            _sme.update_table(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_sme(cls, school_id, sme_id):
        sme = SME.query.filter_by(school_id=school_id, id=sme_id).first()
        if not sme:
            raise CustomException(message="SME not found", status_code=404)

        db.session.delete(sme)
        db.session.commit()
