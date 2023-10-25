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
                    "assigned_teachers": [x.to_dict() for x in project.teachers],
                    **project.to_dict(add_filter=False)
                } for project in results]
            }
        }

        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def search_projects(cls, args, school_id):

        query = Project.query.filter(Project.school_id == int(school_id)).filter(
            (Project.name.ilike(f'%{args}%'))
        )
        result = [
            {
                **x.to_dict(add_filter=False),
                "learning_group": [groups.id for groups in x.learning_groups],
                "email": x.user.email,
                "msisdn": x.user.msisdn,
                "school": x.schools.name,
                "assigned_teachers": [_teacher.to_dict() for _teacher in x.teachers],
            }

            for x in query.all()]
        return result

    @classmethod
    def add_project(cls, school_id, data):
        req: ProjectSchema = validator.validate_data(ProjectSchema, data)

        _school = School.GetSchool(school_id)

        project_exist = Project.query.filter_by(name=req.name, schools=_school).first()

        if project_exist:
            raise CustomException(message="Project with same name already exist", status_code=400)

        school = School.GetSchool(school_id)

        _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, req.group_id)

        try:

            add_project: Project = Project(name=req.name, description=req.description, schools=school, user=current_user)

            _learning_group.projects.append(add_project)

            if req.teacher_id:
                teacher: Teacher = Teacher.GetTeacher(req.teacher_id)
                _learning_group.teachers.append(teacher)
                add_project.teachers.append(teacher)

            if req.student_id:
                for std in req.student_id:
                    student: Student = Student.GetStudent(std)
                    _learning_group.students.append(student)
                    add_project.students.append(student)

            add_project.save(refresh=True)

        except Exception as e:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
        return f"The school project : {req.name} has been added successfully"

    @classmethod
    def update_project(cls, school_id, project_id, data):
        project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.update_table(data)
        return project.to_dict(add_filter=False)

    @classmethod
    def delete_project(cls, school_id, project_id):
        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        db.session.delete(project)
        db.session.commit()
        return "Project has been deleted"

    @classmethod
    def deactivate_project(cls, school_id, project_id, reason):
        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.isDeactivated = not project.isDeactivated
        project.deactivate_reason = reason
        db.session.commit()
        return "Project has been deactivated" if project.isDeactivated else "Project has been activated"

    @classmethod
    def view_project_detail(cls, school_id, project_id):
        _project: Project = Project.GetProject(school_id, project_id)
        return {
            "email": _project.user.email,
            "msisdn": _project.user.msisdn,
            "school": _project.schools.name,
            "learning_groups": [x.id for x in _project.learning_groups],
            "assigned_teachers": [x.to_dict() for x in _project.teachers],
            **_project.to_dict(add_filter=False)
        }
