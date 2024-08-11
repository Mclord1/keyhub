from . import *


class KeywordModel:

    @classmethod
    def create_keyword(cls, data):
        if "name" not in data:
            raise CustomException(message="name is required", status_code=400)

        try:
            keyword = Keywords(**data)
            keyword.save(refresh=True)
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A keyword with that name already exists", status_code=400)
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_all_keywords(cls):
        keywords = Keywords.query.all()
        keyword_list = [keyword.to_dict(add_filter=False) for keyword in keywords]
        return keyword_list

    @classmethod
    def update_keyword(cls, keyword_id, data):
        keyword = Keywords.query.filter_by(id=keyword_id).first()
        if not keyword:
            raise CustomException(message="Keyword not found", status_code=404)

        if "name" not in data:
            raise CustomException(message="name is required", status_code=400)

        try:
            keyword.update_table(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_keyword(cls, keyword_id):
        keyword = Keywords.query.filter_by(id=keyword_id).first()
        if not keyword:
            raise CustomException(message="Keyword not found", status_code=404)

        db.session.delete(keyword)
        db.session.commit()
