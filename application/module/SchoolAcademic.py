from pydantic import constr

from . import *


class AcademicSchema(BaseModel):
    name: constr(max_length=200)


class SchoolAcademicModel:

    @classmethod
    def create_school_academic(cls, school_id, data):
        academicSchema: AcademicSchema = validator.validate_data(AcademicSchema, data)

        _school = School.GetSchool(school_id)

        try:
            academic_model = AcademicYear(name=academicSchema.name, schools=_school)
            academic_model.save(refresh=True)
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_school_academics(cls, school_id):
        _academic = AcademicYear.query.filter_by(school_id=school_id).all()
        academics_list = [academic.to_dict(add_filter=False) for academic in _academic] if _academic else []
        return academics_list

    @classmethod
    def get_single_academic(cls, academic_id, school_id):
        _academics = AcademicYear.query.filter_by(school_id=school_id, id=academic_id).first()

        if _academics and _academics.school_id != int(school_id):
            raise CustomException(message="Academic not found", status_code=404)

        if not _academics:
            raise CustomException(message="Academic not found", status_code=404)
        return _academics.to_dict(add_filter=False)

    @classmethod
    def update_school_academic(cls, academic_id, school_id, data):
        _academics = AcademicYear.query.filter_by(school_id=school_id, id=academic_id).first()

        if _academics and _academics.school_id != int(school_id):
            raise CustomException(message="Academic not found", status_code=404)

        if not _academics:
            raise CustomException(message="Academic not found", status_code=404)

        try:
            _academics.update_table(data)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_school_academic(cls, academic_id, school_id):
        _academics = AcademicYear.query.filter_by(school_id=school_id, id=academic_id).first()

        if _academics and _academics.school_id != int(school_id):
            raise CustomException(message="Term not found", status_code=404)

        if not _academics:
            raise CustomException(message="Term not found", status_code=404)

        try:
            db.session.delete(_academics)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
