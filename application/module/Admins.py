from . import *


class SystemAdmins:
    def __init__(self):
        pass

    @classmethod
    def create_admin(cls, data):

        req: SystemAdminSchema = validator.validate_data(SystemAdminSchema, data)

        user: User = db.session.query(User).filter(
            (User.email == req.email) or (User.msisdn == req.msisdn)
        ).first()

        if user:
            raise CustomException(
                message="The Email or Phone number already registered with other user.",
                status_code=400
            )

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
    def generate_token(cls):
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def reset_password(cls, user_id):
        user: User = User.query.filter_by(id=user_id).first()

        if not user:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        otp_code = cls.generate_token()
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
        add_to_confirmation = ConfirmationCode(email=user.email, user_id=user.id, code=otp_code,
                                               expiration=expiration_time)
        add_to_confirmation.save(refresh=True)
        # TODO :: Send OTP to users email or phone_number
        return f"OTP code has been sent to {user.email}"

    @classmethod
    def get_all_admin(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        role = Role.GetRoleByName('system_admin')
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
        _user: User = User.GetUser(user_id)
        _user.admins.update_table(data)
        return _user.admins.to_dict()

    @classmethod
    def deactivate_user(cls, user_id, reason):
        _user: User = User.GetUser(user_id)

        if _user.isDeactivated:
            raise CustomException(message="Admin account has already been deactivated", status_code=400)

        _user.isDeactivated = True
        _user.deactivate_reason = reason
        db.session.commit()
        return f"{_user.email} account has been deactivated"

    @classmethod
    def search_admin(cls, args):

        query = Admin.query.join(User).filter(
            (Admin.first_name.ilike(f'%{args}%') | Admin.last_name.ilike(f'%{args}%'))
            | User.email.ilike(f'%{args}%')
        )
        result = [x.to_dict() | x.user.to_dict() for x in query.all()]

        for item in result:
            item.pop("password", None)
            item.pop("id", None)

        return result or []


class SchoolAdmins:
    def __init__(self):
        pass
