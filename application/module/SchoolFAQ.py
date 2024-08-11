from . import *


class FAQEntry(BaseModel):
    question: str
    answer: str


class FAQSchema(BaseModel):
    faqs: List[FAQEntry]


class FAQModel:

    @classmethod
    def create_faq(cls, school_id, data):
        faqSchema: FAQSchema = validator.validate_data(FAQSchema, data)

        _school = School.GetSchool(school_id)

        try:
            for faq_item in faqSchema.faqs:
                faq = FAQ(question=faq_item.question, answer=faq_item.answer, schools=_school)
                db.session.add(faq)

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_faqs(cls, school_id):
        faqs = FAQ.query.filter_by(school_id=school_id).all()
        faq_list = [faq.to_dict(add_filter=False) for faq in faqs] if faqs else []
        return faq_list

    @classmethod
    def update_faq(cls, faq_id, school_id, data):
        _faq = FAQ.query.filter_by(school_id=school_id, id=faq_id).first()

        if _faq and _faq.school_id != int(school_id):
            raise CustomException(message="FAQ not found", status_code=404)

        if not _faq:
            raise CustomException(message="FAQ not found", status_code=404)

        try:
            _faq.update_table(data)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_faq(cls, faq_id, school_id):
        _faq: FAQ = FAQ.query.filter_by(school_id=school_id, id=faq_id).first()

        if _faq and _faq.school_id != int(school_id):
            raise CustomException(message="FAQ not found", status_code=404)

        if not _faq:
            raise CustomException(message="FAQ not found", status_code=404)

        try:
            _faq.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
