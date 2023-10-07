from . import *


class ParentModel:

    @classmethod
    def get_all_parents(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        role = Role.GetRoleByName(BasicRoles.PARENT.value)
        _parents = User.query.filter_by(role_id=role.id).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _parents.total
        results = [item for item in _parents.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_parents": len([x for x in results if x.isDeactivated]),
                "num_of_active_parents": len([x for x in results if not x.isDeactivated]),
                "num_of_parents": len(results),
                "parents": [{
                    **res.parents.to_dict(),
                    **res.as_dict(),
                    "num_of_children": len(res.parents.students),
                    "num_of_active_children": len([x for x in res.parents.students if not x.user.isDeactivated]),
                    "num_of_deactivated_children": len([x for x in res.parents.students if x.user.isDeactivated]),
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        _parent: Parent = Helper.get_user(Parent, user_id)
        gender = data.get('gender')
        if gender:
            _parent.gender = gender
        _parent.update_table(data)
        return _parent.to_dict()

    @classmethod
    def add_parent(cls, data):
        req: ParentSchema = validator.validate_data(ParentSchema, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.PARENT.value)

        _student = None
        if req.student:
            _student = Student.GetStudent(req.student)

            if _student.parents:
                raise CustomException(message="A Parent has already been assigned to this parent", status_code=400)

            if not _student:
                raise CustomException(message="Student not found", status_code=404)

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
                    students=[_student]
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
