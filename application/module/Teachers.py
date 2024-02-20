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

        if not current_user.admins or (current_user.managers and current_user.managers.school_id != school.id):
            raise CustomException(message="You do not have privilege to access this school")

        try:
            new_teacher = User.CreateUser(req.email, req.msisdn, role)

            if new_teacher:
                add_user = Teacher(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_teacher.id,
                    address=req.address,
                    gender=req.gender,
                    years_of_experience=req.years_of_experience,
                    has_bachelors_degree=req.has_bachelors_degree,
                    early_years_education=req.early_years_education,
                    linkedin=req.linkedin,
                    how_you_heard_about_us=req.how_you_heard_about_us,
                    purpose_using_the_app=req.purpose_using_the_app,
                    schools=[school]
                )

                add_user.save(refresh=True)
                Audit.add_audit('Added Teacher', current_user, add_user.to_dict())

                return {**add_user.to_dict(), "user_id": add_user.user.id}

        except Exception as e:
            print(e)
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

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

        return {
            **_user.to_dict(),
            **_user.user.as_dict(),
            "user_id": user.id,
            "total_projects": len([x for x in _user.projects]) if _user.projects else 0,
            "projects": [x.to_dict(add_filter=False) for x in _user.projects],
            "total_students": len([x for x in _user.students]) if _user.students else 0,
            "students": [x.to_dict() for x in _user.students],
            "schools": [x.name for x in _user.schools]
        }
