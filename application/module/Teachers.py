from . import *


class TeacherModel:

    @classmethod
    def get_all_teachers(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        role = Role.GetRoleByName(BasicRoles.TEACHER.value)
        _teachers = User.query.filter_by(role_id=role.id).paginate(page=page, per_page=per_page)
        total_items = _teachers.total
        results = [item for item in _teachers.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "total_deactivated_teachers": len([x for x in results if x.isDeactivated]),
                "total_active_teachers": len([x for x in results if not x.isDeactivated]),
                "num_of_teachers": len(results),
                "teachers": [{
                    **res.teachers.to_dict(),
                    **res.as_dict(),
                    "total_projects": len(res.teachers.projects),
                    "total_students": len(res.teachers.students),
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        _teacher: Teacher = Helper.get_user(Teacher, user_id)
        gender = data.get('gender')
        role = data.get('role')
        if role:
            _teacher.user.role_id = role
        if gender:
            _teacher.gender = gender
        _teacher.update_table(data)
        return _teacher.to_dict()

    @classmethod
    def add_teacher(cls, data):
        req: TeacherSchema = validator.validate_data(TeacherSchema, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.TEACHER.value)

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
                    schools=[school]
                )
                add_user.save(refresh=True)
                return add_user

        except Exception as e:
            print(e)
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def reset_password(cls, user_id):
        _teacher: Teacher = Helper.get_user(Teacher, user_id)
        if not _teacher:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _teacher.user

        return Helper.send_otp(_user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        _teacher: Teacher = Helper.get_user(Teacher, user_id)

        if not _teacher:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _teacher.user

        return Helper.disable_account(_user, reason)

    @classmethod
    def search_teachers(cls, args):
        return Helper.look_up_account(Teacher, User, args)
