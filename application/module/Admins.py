from . import *


class SystemAdmins:

    @classmethod
    def create_admin(cls, data):

        req: SystemAdminSchema = validator.validate_data(SystemAdminSchema, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRole(req.role)

        try:
            new_admin = User.CreateUser(req.email, req.msisdn, role)

            if new_admin:
                add_user = Admin(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_admin.id,
                    residence=req.address,
                    gender=req.gender,
                )
                add_user.save(refresh=True)
                return add_user

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def get_all_admin(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        role = Role.GetRoleByName(BasicRoles.SYSTEM_ADMIN)
        _admin = User.query.filter_by(role_id=role.id).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _admin.total
        results = [item.admins.to_dict() | item.to_dict() for item in _admin.items]
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
    def update_admin(cls, user_id, data):
        _admin: Admin = Admin.GetAdmin(user_id)
        _admin.update_table(data)
        return _admin.to_dict()

    @classmethod
    def reset_password(cls, user_id):
        _admin: Admin = Admin.GetAdmin(user_id)

        if not admin:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _admin.user

        return Helper.send_otp(_user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        _admin: Admin = Admin.GetAdmin(user_id)

        if not admin:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _admin.user

        return Helper.disable_account(_user, reason)

    @classmethod
    def search_admin(cls, args):
        return Helper.look_up_account(Admin, User, args)
