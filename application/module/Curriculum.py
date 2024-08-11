from . import *


class CurriculumModel:

    @classmethod
    def create_curriculum(cls, data):
        if "name" not in data:
            raise CustomException(message="name is required", status_code=400)

        try:
            Curriculum = Curriculums(**data)
            Curriculum.save(refresh=True)
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A Curriculum with that name already exists", status_code=400)
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_all_curriculum(cls):
        Curriculum = Curriculums.query.all()
        Curriculum_list = [x.to_dict(add_filter=False) for x in Curriculum]
        return Curriculum_list

    @classmethod
    def update_curriculum(cls, Curriculum_id, data):
        Curriculum = Curriculums.query.filter_by(id=Curriculum_id).first()
        if not Curriculum:
            raise CustomException(message="Curriculum not found", status_code=404)

        if "name" not in data:
            raise CustomException(message="name is required", status_code=400)

        try:
            Curriculum.update_table(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_curriculum(cls, Curriculum_id):
        Curriculum = Curriculums.query.filter_by(id=Curriculum_id).first()
        if not Curriculum:
            raise CustomException(message="Curriculum not found", status_code=404)

        db.session.delete(Curriculum)
        db.session.commit()
