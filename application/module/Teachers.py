import ast

from sqlalchemy import or_

from . import *


class TeacherModel:

    @classmethod
    def get_all_teachers(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _teachers = Teacher.query.order_by(desc(Teacher.created_at)).paginate(page=page, per_page=per_page)
        total_items = _teachers.total
        results = [item for item in _teachers.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "total_deactivated_teachers": len([x for x in results if x.user.isDeactivated]),
                "total_active_teachers": len([x for x in results if not x.user.isDeactivated]),
                "num_of_teachers": len(results),
                "teachers": [{
                    **(res.user.as_dict() if res.user else {}),
                    **res.to_dict(),
                    "user_id": res.user.id,
                    "school": [x.name for x in res.schools],
                    "total_projects": len([x for x in res.projects]) if res.projects else 0,
                    "learning_groups": [{'name': x.name, 'id': x.id} for x in res.learning_groups],
                    "total_students": len([x for x in res.students]) if res.students else 0,
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        user: User = User.GetUser(user_id)

        if not user.teachers:
            raise CustomException(message="Teacher does not exist", status_code=404)

        gender = data.get('gender')
        role = data.get('role')
        if role:
            user.role_id = role
        if gender:
            user.teachers.gender = gender
        user.teachers.update_table(data)
        Audit.add_audit('Updated Teacher Information', current_user, user.teachers.to_dict())

        return {**user.teachers.to_dict(), "user_id": user.id}

    @classmethod
    def add_teacher(cls, data):
        req: TeacherSchema = validator.validate_data(TeacherSchema, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.TEACHER.value)

        school = School.GetSchool(req.school_id)

        if not current_user.admins and (current_user.managers and current_user.managers.school_id != school.id):
            raise CustomException(message="You do not have privilege to access this school")

        if req.profile_image:

            file_path = FileFolder.teacher_profile(school.name, req.email)

            profile_url = FileHandler.upload_file(req.profile_image, file_path)
        else:
            profile_url = None

        new_teacher = User.CreateUser(req.email, req.msisdn, role)

        try:

            if new_teacher:
                add_user = Teacher(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_teacher.id,
                    address=req.address,
                    gender=req.gender,
                    profile_image=profile_url,
                    years_of_experience=req.years_of_experience,
                    has_bachelors_degree=req.has_bachelors_degree,
                    early_years_education=req.early_years_education,
                    linkedin=req.linkedin,
                    how_you_heard_about_us=req.how_you_heard_about_us,
                    purpose_using_the_app=req.purpose_using_the_app,
                    schools=[school]
                )

                if req.learning_group_id:
                    _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(req.school_id, req.learning_group_id)

                    _learning_group.teachers.append(add_user)

                add_user.save(refresh=True)
                Audit.add_audit('Added Teacher', current_user, add_user.to_dict())
                EmailHandler.welcome_mail(new_teacher.email, add_user.first_name)
                return {**add_user.to_dict(), "user_id": add_user.user.id}

        except Exception as e:
            if new_teacher:
                db.session.delete(new_teacher)
            db.session.rollback()
            raise e

    @classmethod
    def change_teacher_profile_image(cls, profile_image, teacher_id):
        if not profile_image:
            raise CustomException(message="User profile image is required")

        user: User = User.GetUser(teacher_id)

        if not user.teachers:
            raise CustomException(message="Teacher does not exist", status_code=404)

        file_path = FileFolder.teacher_profile(user.teachers.schools[0].name, user.email)

        profile_url = FileHandler.upload_file(profile_image, file_path)

        user.teachers.profile_image = profile_url
        db.session.commit()
        return "Profile Image has been updated successfully"

    @classmethod
    def reset_password(cls, user_id):
        user: User = User.GetUser(user_id)

        if not user.teachers:
            raise CustomException(message="Teacher does not exist", status_code=404)

        Audit.add_audit('Reset Teacher Password', current_user, user.to_dict())

        return Helper.send_otp(user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        user: User = User.GetUser(user_id)

        if not user.teachers:
            raise CustomException(message="Teacher does not exist", status_code=404)

        Audit.add_audit('Changed Teacher Account Status', current_user, user.to_dict())

        return Helper.disable_account(user, reason)

    @classmethod
    def search_teachers(cls, args):
        return Helper.look_up_account(Teacher, User, args)

    @classmethod
    def get_user(cls, user_id):

        user: User = User.GetUser(user_id)

        if not user.teachers:
            raise CustomException(message="Teacher does not exist", status_code=404)

        _user: Teacher = Helper.get_user(Teacher, user.teachers.id)

        _user_id = _user.user.id

        _projects = Project.query.filter(
            or_(
                Project.lead_teacher == _user_id,
                Project.supporting_teachers.contains(str(_user_id))
            )
        ).all()

        return {
            **_user.to_dict(),
            **_user.user.as_dict(),
            "user_id": user.id,
            "total_projects": len(_projects) if _projects else 0,
            "learning_groups": [{'name': x.name, 'id': x.id} for x in _user.learning_groups],
            "projects": [x.to_dict(add_filter=False) for x in _projects],
            "total_students": len([x for x in _user.students]) if _user.students else 0,
            "students": [x.to_dict() for x in _user.students],
            "schools": [x.name for x in _user.schools]
        }
