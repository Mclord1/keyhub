from . import *


class ParentModel:

    @classmethod
    def get_all_parents(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _parents = Parent.query.order_by(desc(Parent.created_at)).paginate(page=page, per_page=per_page,
                                                                           error_out=False)
        total_items = _parents.total
        results = [item for item in _parents.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_parents": len([x for x in results if x.user.isDeactivated]),
                "num_of_active_parents": len([x for x in results if not x.user.isDeactivated]),
                "num_of_parents": len(results),
                "parents": [{
                    **(res.user.as_dict() if res.user else {}),
                    **res.to_dict(),
                    "num_of_children": len(res.students) if res and res.students else 0,
                    "num_of_active_children": len([x for x in res.students if not x.user.isDeactivated]),
                    "num_of_deactivated_children": len([x for x in res.students if x.user.isDeactivated]),
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        _parent: Parent = Helper.get_user(Parent, user_id)
        gender = data.get('gender')
        role = data.get('role')
        if role:
            _parent.user.role_id = role
        if gender:
            _parent.gender = gender
        _parent.update_table(data)
        return _parent.to_dict()

    @classmethod
    def add_parent(cls, data):
        req: ParentSchema = validator.validate_data(ParentSchema, data)

        a = Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.PARENT.value)

        if req.student:

            for std in req.student:

                _student: Student = Student.GetStudent(std)

                if _student.parents:
                    raise CustomException(
                        message=f"A Parent has already been assigned to {_student.first_name} {_student.last_name}",
                        status_code=400)

        try:
            new_parent = User.CreateUser(req.email, req.msisdn, role)

            if new_parent:
                add_user = Parent(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_parent.id,
                    address=req.address,
                    gender=req.gender,
                    work_email=req.work_email,
                    work_address=req.work_address,
                    work_msisdn=req.work_msisdn,
                    students=[Student.GetStudent(x) for x in req.student]
                )
                add_user.save(refresh=True)
                return add_user

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def reset_password(cls, user_id):
        _parent: Parent = Helper.get_user(Parent, user_id)

        if not _parent:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _parent.user

        return Helper.send_otp(_user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        _parent: Parent = Helper.get_user(Parent, user_id)

        if not _parent:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _parent.user

        return Helper.disable_account(_user, reason)

    @classmethod
    def search_parents(cls, args):
        return Helper.look_up_account(Parent, User, args)

    @classmethod
    def get_user(cls, user_id):
        _user = Helper.get_user(Parent, user_id)
        return {
            **_user.to_dict(),
            "students" : [x.to_dict() for x in _user.students]
        }
