from pydantic import constr

from . import *


class TermsSchema(BaseModel):
    name: constr(max_length=200)


class SchoolTermsModel:

    @classmethod
    def create_school_terms(cls, school_id, data):
        terms: TermsSchema = validator.validate_data(TermsSchema, data)

        _school = School.GetSchool(school_id)

        try:
            terms_model = Term(name=terms.name, schools=_school)
            terms_model.save(refresh=True)
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_school_terms(cls, school_id):
        _terms = Term.query.filter_by(school_id=school_id).all()
        terms_list = [term.to_dict(add_filter=False) for term in _terms] if _terms else []
        return terms_list

    @classmethod
    def get_single_term(cls, term_id, school_id):
        _terms = Term.query.filter_by(school_id=school_id, id=term_id).first()

        if _terms and _terms.school_id != int(school_id):
            raise CustomException(message="Term not found", status_code=404)

        if not _terms:
            raise CustomException(message="Term not found", status_code=404)
        return _terms.to_dict(add_filter=False)

    @classmethod
    def update_school_term(cls, term_id, school_id, data):
        _terms = Term.query.filter_by(school_id=school_id, id=term_id).first()

        if _terms and _terms.school_id != int(school_id):
            raise CustomException(message="Term not found", status_code=404)

        if not _terms:
            raise CustomException(message="Term not found", status_code=404)

        try:
            _terms.update_table(data)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_school_term(cls, term_id, school_id):
        _terms = Term.query.filter_by(school_id=school_id, id=term_id).first()

        if _terms and _terms.school_id != int(school_id):
            raise CustomException(message="Term not found", status_code=404)

        if not _terms:
            raise CustomException(message="Term not found", status_code=404)

        try:
            db.session.delete(_terms)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
