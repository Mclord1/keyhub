from . import *


class SystemAdmins:
    def __init__(self):
        pass

    @classmethod
    def CreateAdmin(cls, data):

        req: SystemAdminSchema = validator.validate_data(SystemAdminSchema, data)

        user: User = db.session.query(User).filter(
            (User.email == req.email) or (User.msisdn == req.msisdn)
        ).first()

        if user:
            raise CustomException(message="The Email or Phone number already registered with other user. ", status_code=400)

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
                db.session.add(add_user)
                db.session.commit()
                db.session.refresh(add_user)

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def generate_token(cls):
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def ResetPassword(cls, user_id):
        user: User = User.query.filter_by(id=user_id).first()

        if not user:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        otp_code = cls.generate_token()
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
        add_to_confirmation = ConfirmationCode(email=user.email, user_id=user.id, code=otp_code, expiration=expiration_time)
        add_to_confirmation.save(refresh=True)
        # TODO :: Send OTP to users email or phone_number
        return f"OTP code has been sent to {user.email}"

    @classmethod
    def GetAllAdmin(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _admin = Admin.query.paginate(page=page, per_page=per_page, error_out=False)
        total_items = _admin.total
        results = [item.to_dict() for item in _admin.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": json.loads(json.dumps(results, default=enum_serializer))
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def UpdateAdmin(cls):
        pass

    @classmethod
    def DeleteAdmin(cls):
        pass

    @classmethod
    def SearchAdmin(cls, name=None, email=None):
        query = None
        if name:
            query = Admin.query.filter(Admin.first_name.ilike(f'%{name}%'))
        if email:
            query = User.query.filter(User.email.ilike(f'%{email}%'))

        return query.all()


class SchoolAdmins:
    def __init__(self):
        pass
