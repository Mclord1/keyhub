from . import *


class TeacherModel:

    @classmethod
    def get_all_teachers(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        role = Role.GetRoleByName(BasicRoles.TEACHER)
        _teachers = User.query.filter_by(role_id=role.id).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _teachers.total
        results = [item.teachers.to_dict() | item.to_dict() for item in _teachers.items]
        total_pages = (total_items - 1) // per_page + 1

        for item in results:
            item.pop("password", None)
            item.pop("id", None)

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": results
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        _teacher: Teacher = Teacher.GetTeacher(user_id)
        _teacher.update_table(data)
        return _teacher.to_dict()

    @classmethod
    def add_teacher(cls, data):
        req: TeacherSchema = validator.validate_data(TeacherSchema, data)

        user: User = db.session.query(User).filter(
            (User.email == req.email) or (User.msisdn == req.msisdn)
        ).first()

        if user:
            raise CustomException(
                message="The Email or Phone number already registered with other user.",
                status_code=400
            )

        role = Role.GetRoleByName(BasicRoles.TEACHER)

        school = School.GetSchool(req.school_id)

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
                    schools=school
                )
                add_user.save(refresh=True)
                return add_user

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def reset_password(cls, user_id):
        _teacher: Teacher = Teacher.GetTeacher(user_id)

        if not _teacher:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _teacher.user

        return Helper.send_otp(_user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        _teacher: Teacher = Teacher.GetTeacher(user_id)

        if not _teacher:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _teacher.user

        return Helper.disable_account(_user, reason)

    @classmethod
    def search_teachers(cls, args):
        return Helper.look_up_account(Teacher, User, args)
