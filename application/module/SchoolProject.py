from . import *
from ..Schema.school import ProjectSchema


class SchoolProjectModel:

    @classmethod
    def get_projects(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _project: Project = Project.query.filter(Project.school_id == school_id).order_by(
            desc(Project.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _project.total
        results = [item for item in _project.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_projects": len(results),
                "num_of_active_projects": len([x for x in results if not x.isDeactivated]),
                "num_of_deactivated_projects": len([x for x in results if x.isDeactivated]),
                "projects": [{
                    # "num_of_students": sum([ x.s for x in project.learning_group_projects]),
                    "email": project.user.email,
                    "msisdn": project.user.msisdn,
                    "school": project.schools.name,
                    "assigned_teachers": [x.teachers.to_dict() for x in project.learning_group_projects],
                    **project.to_dict()
                } for project in results]
            }
        }

        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def search_projects(cls, args, school_id):

        query = Project.query.filter(Project.school_id == int(school_id)).filter(
            (Project.name.ilike(f'%{args}%'))
        )
        result = [x.to_dict() for x in query.all()]
        return result

    @classmethod
    def add_project(cls, school_id, data):
        req: ProjectSchema = validator.validate_data(ProjectSchema, data)

        project_exist = Project.query.filter_by(name=req.name).first()

        if project_exist:
            raise CustomException(message="Project with same name already exist", status_code=400)

        student = Student.GetStudent(req.student_id)
        teacher = Teacher.GetTeacher(req.teacher_id)
        school = School.GetSchool(school_id)
        _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, req.group_id)
        try:
            add_project = Project(name=req.name, description=req.description, schools=school, user=current_user)
            add_project.save(refresh=True)
            add_group_project = LearningGroupProjects(teachers=teacher, students=student, projects=add_project, learning_group=_learning_group)
            add_group_project.save(refresh=True)
        except Exception as e:
            print(e)
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
        return f"The school project : {req.name} has been added successfully"

    @classmethod
    def update_project(cls, school_id, project_id, data):
        project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.update_table(data)
        return project.to_dict()

    @classmethod
    def delete_project(cls, school_id, project_id):
        project : Project = Project.GetProject(school_id=school_id, project_id=project_id)

        if project.learning_group_projects:
            raise CustomException(message="There are students and teachers linked to this project")

        db.session.delete(project)
        db.session.commit()
        return "Project has been deleted"

    @classmethod
    def deactivate_project(cls, school_id, project_id, reason):
        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.isDeactivated = not project.isDeactivated
        project.deactivate_reason = reason
        db.session.commit()
        return "Project has been deactivated"

    @classmethod
    def view_project_detail(cls, school_id, project_id):
        _project = Project.GetProject(school_id,project_id)
        return {
            "email": _project.user.email,
            "msisdn": _project.user.msisdn,
            "school": _project.schools.name,
            "assigned_teachers": [x.teachers.to_dict() for x in _project.learning_group_projects],
            **_project.to_dict()
        }
