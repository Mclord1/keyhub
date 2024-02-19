import ast

from . import *
from ..Schema.school import ProjectSchema, UpdateProjectSchema


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
                    # "num_of_students": len([ x.s for x in project.learning_group_projects]),
                    "email": project.user.email,
                    "msisdn": project.user.msisdn,
                    "school": project.schools.name,
                    "activities": [activity.to_dict(add_filter=False) for activity in project.activities],
                    **project.to_dict(add_filter=False),
                    "lead_teacher": Teacher.GetTeacher(project.lead_teacher).to_dict() if project.lead_teacher else None,
                    "supporting_teachers": [Teacher.GetTeacher(x).to_dict() for x in
                                            ast.literal_eval(project.supporting_teachers)] if project.supporting_teachers is not None else None,
                } for project in results]
            }
        }

        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def search_projects(cls, args, school_id):
        query = Project.query.filter(Project.school_id == int(school_id), Project.status == 'approved').filter(
            (Project.name.ilike(f'%{args}%'))
        )
        result = [
            {
                **x.to_dict(add_filter=False),
                "learning_group": [groups.id for groups in x.learning_groups],
                "email": x.user.email,
                "msisdn": x.user.msisdn,
                "school": x.schools.name,
                "students": [x.to_dict() for x in x.students],
                "activities": [activity.to_dict(add_filter=False) for activity in x.activities],
                "lead_teacher": Teacher.GetTeacher(x.lead_teacher).to_dict() if x.lead_teacher else None,
                "supporting_teachers": [Teacher.GetTeacher(x).to_dict() for x in
                                        ast.literal_eval(x.supporting_teachers)] if x.supporting_teachers is not None else None,
            }

            for x in query.all()]
        return result

    @classmethod
    def search_all_school_projects(cls, args):

        if not current_user.admins:
            raise CustomException(message="You don't have permission to access this service.")

        query = Project.query.filter(
            (Project.name.ilike(f'%{args}%'))
        ).filter(Project.is_private.is_(False), Project.status == 'approved')
        result = [
            {
                **x.to_dict(add_filter=False),
                "learning_group": [groups.id for groups in x.learning_groups],
                "email": x.user.email,
                "msisdn": x.user.msisdn,
                "school": x.schools.name,
                "students": [x.to_dict() for x in x.students],
                "activities": [activity.to_dict(add_filter=False) for activity in x.activities],
                "lead_teacher": Teacher.GetTeacher(x.lead_teacher).to_dict() if x.lead_teacher else None,
                "supporting_teachers": [Teacher.GetTeacher(x).to_dict() for x in
                                        ast.literal_eval(x.supporting_teachers)] if x.supporting_teachers is not None else None,
            }

            for x in query.all()]
        return result

    @classmethod
    def add_project(cls, school_id, data):

        req: ProjectSchema = validator.validate_data(ProjectSchema, data)
        _school = School.GetSchool(school_id)
        project_exist: Project = Project.query.filter_by(name=req.name, schools=_school).first()

        if project_exist:
            raise CustomException(message="Project with same name already exist", status_code=400)

        school = School.GetSchool(school_id)

        try:

            spread_in_project = {x: data[x] for x in data if x not in ['group_id', 'student_id', 'teacher_id']}
            add_project: Project = Project(**spread_in_project, schools=school, user=current_user)

            for group in req.group_id:
                _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group)

                student_list = data.get('student_id', [])
                _students = Student.query.filter(Student.id.in_(student_list)).all()

                _learning_group.students.extend(_students)
                add_project.students.extend(_students)

                _learning_group.projects.append(add_project)

                subscribed_users = [x.user_id for x in _learning_group.subscribed_groups]
                Notification.send_push_notification(subscribed_users, f"{req.name} project has been added to the learning group", LearningGroup.__name__)

            add_project.save(refresh=True)
            Audit.add_audit('Added School Project', current_user, add_project.to_dict(add_filter=False))

            return add_project.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def update_project(cls, school_id, project_id, data):
        project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.update_table(data)
        Audit.add_audit('Updated School Project Information', current_user, project.to_dict(add_filter=False))
        return project.to_dict(add_filter=False)

    @classmethod
    def delete_project(cls, school_id, project_id):
        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        db.session.delete(project)
        Audit.add_audit('Deleted School Project', current_user, project.to_dict(add_filter=False))
        subscribed_users = [subs.user_id for x in project.learning_groups for subs in x.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{project.name} project has been removed from the learning group", LearningGroup.__name__)
        db.session.commit()
        return "Project has been deleted"

    @classmethod
    def approve_project(cls, school_id, project_id):
        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.status = "approved"
        Audit.add_audit('Approved School Project', current_user, project.to_dict(add_filter=False))
        subscribed_users = [subs.user_id for x in project.learning_groups for subs in x.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{project.name} project has been approved", LearningGroup.__name__)
        db.session.commit()
        return "Project has been approved"

    @classmethod
    def deactivate_project(cls, school_id, project_id, reason):
        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        project.isDeactivated = not project.isDeactivated
        project.deactivate_reason = reason
        db.session.commit()
        Audit.add_audit("Deactivated School Project" if project.isDeactivated else "Activate School Project", current_user, project.to_dict(add_filter=False))

        subscribed_users = [subs.user_id for x in project.learning_groups for subs in x.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{project.name} project has been deactivated from the learning group", LearningGroup.__name__)

        return "Project has been deactivated" if project.isDeactivated else "Project has been activated"

    @classmethod
    def view_project_detail(cls, school_id, project_id):
        _project: Project = Project.GetProject(school_id, project_id)
        return {
            "email": _project.user.email,
            "msisdn": _project.user.msisdn,
            "school": _project.schools.name,
            "students": [x.to_dict() for x in _project.students],
            "sme": [x.to_dict(add_filter=False) for x in _project.schools.smes],
            "activities": [x.to_dict(add_filter=False) for x in _project.activities],
            "learning_groups": [x.to_dict(add_filter=False) for x in _project.learning_groups],
            **_project.to_dict(add_filter=False),
            "learning_goals": list(_project.learning_goals) if _project.learning_goals else [],
            "lead_teacher": Teacher.GetTeacher(_project.lead_teacher).to_dict() if _project.lead_teacher else None,
            "supporting_teachers": [Teacher.GetTeacher(x).to_dict() for x in
                                    ast.literal_eval(_project.supporting_teachers)] if _project.supporting_teachers is not None else None,
        }

    @classmethod
    def assign_user_to_project(cls, school_id, project_id, data, model):

        req: UpdateProjectSchema = validator.validate_data(UpdateProjectSchema, data)

        project_id = int(project_id)
        model = model.lower()

        _project: Project = Project.GetProject(school_id=school_id, project_id=project_id)

        _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, req.group_id)

        try:
            if model == "teacher":
                if not req.teacher_type or str(req.teacher_type).lower() not in ("lead_teacher", "support_teacher"):
                    raise CustomException(message="teacher_type i must be either lead_teacher or support_teacher", status_code=400)
                for _user in req.users:

                    _teacher: Teacher = Teacher.GetTeacher(_user)

                    if _learning_group.school_id not in [x.id for x in _teacher.schools]:
                        raise CustomException(message="The teacher doesn't belong to learning group school", status_code=400)

                    if _project.students:
                        # append students to teacher if project students exist
                        _teacher.students.extend(_project.students)

                    if _teacher not in _learning_group.teachers:
                        # Add teacher to a learning group if teacher don't belong to a learning group
                        _learning_group.teachers.append(_teacher)

                    if req.teacher_type.lower() == "lead_teacher":
                        _project.lead_teacher = _teacher.id

                    if req.teacher_type.lower() == "support_teacher":

                        if _project.supporting_teachers:
                            new_member = ast.literal_eval(_project.supporting_teachers)
                            if _teacher.id not in new_member:
                                new_member.append(_teacher.id)

                        else:
                            new_member = [_teacher.id]

                        _project.supporting_teachers = str(new_member)

                    _project.teachers.append(_teacher)

                    Audit.add_audit('Assigned Teacher to School Project', current_user, _project.to_dict(add_filter=False))

            if model == "student":

                for _user in req.users:
                    _student: Student = Student.GetStudent(_user)

                    if _learning_group.school_id != _student.school_id:
                        raise CustomException(message="The student doesn't belong to the learning group school", status_code=400)

                    if _project.teachers:
                        # append teachers to student if project teachers exist
                        _student.teachers.extend(_project.teachers)

                    # Add student to a learning group if student don't belong to a learning group
                    if _student not in _learning_group.students:
                        _learning_group.students.append(_student)

                    _project.students.append(_student)

                    Audit.add_audit('Assigned Student to School Project', current_user, _project.to_dict(add_filter=False))

            db.session.commit()
            return "User has been added to the project"
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def remove_user_from_project(cls, school_id, project_id, data, model):

        req: UpdateProjectSchema = validator.validate_data(UpdateProjectSchema, data)

        project_id = int(project_id)
        model = model.lower()

        project: Project = Project.GetProject(school_id=school_id, project_id=project_id)
        _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, req.group_id)

        try:
            if model == "teacher":
                for _user in req.users:

                    _teacher: Teacher = Teacher.GetTeacher(_user)

                    if len(_teacher.projects) == 1:
                        _learning_group.teachers.append(_teacher)

                    if _teacher not in project.teachers:
                        raise CustomException(message="Teacher doesn't exist in this group", status_code=404)

                    project.teachers.remove(_teacher)

                    Audit.add_audit('Removed Teacher from School Project', current_user, project.to_dict(add_filter=False))

            if model == "student":
                for _user in req.users:

                    _student: Student = Student.GetStudent(_user)

                    if len(_student.projects) == 1:
                        _learning_group.students.remove(_student)

                    if _student not in project.students:
                        raise CustomException(message="Student doesn't exist in this group", status_code=404)

                    project.students.remove(_student)

                    Audit.add_audit('Removed Student from School Project', current_user, project.to_dict(add_filter=False))

            db.session.commit()
            return "User has been removed from the project"
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def add_comment(cls, school_id, project_id, comment):
        project = Project.GetProject(school_id, project_id)
        new_comment = ProjectComment(project_id=project.id, user_id=current_user.id, comment=comment)
        new_comment.save(refresh=True)
        return "Comment has been added successfully"

    @classmethod
    def get_comments(cls, school_id, project_id):
        comments: Project = Project.GetProject(school_id, project_id)
        return [
            {
                **x.to_dict(add_filter=False),
                "commented_by": {
                    **User.GetUserObject(x.user.id)
                },
            }
            for x in comments.project_comments]

    @classmethod
    def edit_comment(cls, project_id, comment_id, new_comment):
        comments: ProjectComment = ProjectComment.query.filter_by(project_id=project_id, id=comment_id).first()
        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers or current_user.id != comments.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        comments.comment = new_comment
        db.session.commit()
        return "Comment has been updated successfully"

    @classmethod
    def remove_comment(cls, project_id, comment_id):
        comments: ProjectComment = ProjectComment.query.filter_by(project_id=project_id, id=comment_id).first()
        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers or current_user.id != comments.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        comments.delete()
        return "Comment has been deleted successfully"

    @classmethod
    def add_file(cls, school_id, project_id, file):
        project: Project = Project.GetProject(school_id, project_id)

        file_path, file_name = FileFolder.project_file(project.schools.name, project.name)

        profile_url = FileHandler.upload_file(file, file_path)

        new_file = ProjectFile(project_id=project.id, file_name=file_name, file_url=profile_url, file_path=file_path, user_id=current_user.id)
        new_file.save()
        return "File has been added successfully"

    @classmethod
    def get_files(cls, school_id, project_id):
        _files: Project = Project.GetProject(school_id, project_id)
        return [
            {
                **x.to_dict(add_filter=False),
                "uploaded_by": x.user.email,
                "file_url": FileHandler.get_file_url(x.file_path)
            }
            for x in _files.project_files]

    @classmethod
    def remove_file(cls, project_id, file_id):
        _files: ProjectFile = ProjectFile.query.filter_by(project_id=project_id, id=file_id).first()
        if not _files:
            raise CustomException(message="File not found", status_code=404)

        if not current_user.managers or current_user.id != _files.user_id:
            if not current_user.admins:
                raise CustomException(message="Only File author or admin can delete this File", status_code=400)

        FileHandler.delete_file(_files.file_path)
        _files.delete()
        return "File has been deleted successfully"
