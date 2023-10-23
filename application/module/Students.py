from . import *


class StudentModel:

    @classmethod
    def get_all_students(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _students = Student.query.order_by(desc(Student.created_at)).paginate(page=page, per_page=per_page,
                                                                              error_out=False)
        total_items = _students.total
        results = [item for item in _students.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_students": len([x for x in results if x.user.isDeactivated]),
                "num_of_active_students": len([x for x in results if not x.user.isDeactivated]),
                "num_of_students": len(results),
                "students": [{
                    **(res.user.as_dict() if res.user else {}),
                    **res.to_dict(),
                    "project": [x.to_dict() for x in res.projects],
                    "parent": {**(res.parents.to_dict() if res.parents else {}),
                               **(res.parents.user.as_dict() if res.parents else {})},
                    "school": res.schools.name,
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        _student: Student = Helper.get_user(Student, user_id)
        gender = data.get('gender')
        role = data.get('role')
        if role:
            _student.user.role_id = role
        if gender:
            _student.gender = gender
        _student.update_table(data)
        return _student.to_dict()

    @classmethod
    def add_student(cls, data):
        req: StudentSchema = validator.validate_data(StudentSchema, data)

        if req.email and req.msisdn:
            Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.STUDENT.value)

        school = School.GetSchool(req.school_id)
        _parent = None
        if req.parent:
            _parent = Parent.GetParent(req.parent)

            if not _parent:
                raise CustomException(message="Parent not found", status_code=404)

        try:
            new_student = User.CreateUser(req.email, req.msisdn, role)

            if new_student:
                add_user = Student(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_student.id,
                    address=req.address,
                    gender=req.gender,
                    dob=req.date_of_birth,
                    age=req.age,
                    schools=school,
                    parents=_parent
                )
                add_user.save(refresh=True)
                return add_user

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def reset_password(cls, user_id):
        _student: Student = Helper.get_user(Student, user_id)

        if not _student:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _student.user

        return Helper.send_otp(_user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        _student: Student = Helper.get_user(Student, user_id)

        if not _student:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _student.user

        return Helper.disable_account(_user, reason)

    @classmethod
    def search_students(cls, args):
        return Helper.look_up_account(Student, User, args)

    @classmethod
    def get_user(cls, user_id):
        _user = Helper.get_user(Student, user_id)
        return {
            **_user.to_dict(),
            **_user.user.as_dict(),
            "parent": _user.parents.to_dict() if _user.parents else {},
            "project": [x.to_dict() for x in _user.projects]
        }
