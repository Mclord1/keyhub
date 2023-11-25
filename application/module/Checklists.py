from . import *


class CheckListModel:

    @classmethod
    def create_checklist(cls, data):
        if "question" not in data:
            raise CustomException(message="question is required", status_code=400)

        try:
            checklist = ChecklistQuestion(**data, created_by=current_user.id)
            checklist.save(refresh=True)
            Audit.add_audit('New Checklist Added', current_user, checklist.to_dict(add_filter=False))
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_all_checklist(cls):
        checklists = ChecklistQuestion.query.filter(ChecklistQuestion.is_private == False).all()
        checklist_list = [checklist.to_dict(add_filter=False) for checklist in checklists]
        return checklist_list

    @classmethod
    def update_checklist(cls, checklist_id, data):
        checklist: ChecklistQuestion = ChecklistQuestion.query.filter_by(id=checklist_id).first()
        if not checklist:
            raise CustomException(message="checklist not found", status_code=404)

        if "question" not in data:
            raise CustomException(message="Question is required", status_code=400)

        try:
            checklist.update_table(data)
            db.session.commit()
            Audit.add_audit('Updated Checklist Added', current_user, checklist.to_dict(add_filter=False))
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_checklist(cls, checklist_id):
        checklist: ChecklistQuestion = ChecklistQuestion.query.filter_by(id=checklist_id).first()
        if not checklist:
            raise CustomException(message="checklist not found", status_code=404)
        Audit.add_audit('Deleted Checklist', current_user, checklist.to_dict(add_filter=False))
        checklist.delete()
