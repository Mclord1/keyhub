from datetime import date

from pydantic import constr

from . import *


class ProjectActivitySchema(BaseModel):
    project_id: int
    name: constr(max_length=200)
    start_date: date
    finish_date: date
    description: str
    learning_objectives: str
    resources: str
    supporting_weblinks: str
    supporting_media: str
    ways_to_extend: str


class ProjectActivityModel:

    @classmethod
    def create_project_activity(cls, school_id, data):
        activity: ProjectActivitySchema = validator.validate_data(ProjectActivitySchema, data)

        _project = Project.query.filter_by(school_id=school_id, id=activity.project_id).first()

        if not _project:
            raise CustomException(message="Project does not exist", status_code=404)

        try:
            activity_model = ProjectActivity(
                name=activity.name,
                start_date=activity.start_date,
                finish_date=activity.finish_date,
                description=activity.description,
                learning_objectives=activity.learning_objectives,
                resources=activity.resources,
                supporting_weblinks=activity.supporting_weblinks,
                supporting_media=activity.supporting_media,
                ways_to_extend=activity.ways_to_extend,
                projects=_project
            )
            db.session.add(activity_model)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_project_activities(cls, school_id, project_id):
        _project = Project.query.filter_by(school_id=school_id, id=project_id).first()
        activity_list = [activity.to_dict(add_filter=False) for activity in _project.activities] if _project else []
        return activity_list

    @classmethod
    def get_project_activity(cls, activity_id, school_id):
        activity = ProjectActivity.query.filter_by(id=activity_id).first()

        if activity and activity.projects.school_id != int(school_id):
            raise CustomException(message="Activity not found", status_code=404)

        if not activity:
            raise CustomException(message="Activity not found", status_code=404)
        return activity.to_dict(add_filter=False)

    @classmethod
    def update_project_activity(cls, activity_id, school_id, data):
        activity = ProjectActivity.query.filter_by(id=activity_id).first()

        if activity and activity.projects.school_id != int(school_id):
            raise CustomException(message="Activity not found", status_code=404)

        if not activity:
            raise CustomException(message="Activity not found", status_code=404)

        try:
            activity.update_table(data)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_project_activity(cls, activity_id, school_id):
        activity = ProjectActivity.query.filter_by(id=activity_id).first()

        if activity and activity.projects.school_id != int(school_id):
            raise CustomException(message="Activity not found", status_code=404)

        if not activity:
            raise CustomException(message="Activity not found", status_code=404)

        try:
            db.session.delete(activity)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
