from . import *
from ..Schema.school import PrimaryContact


class SchoolAdminModel:

    @classmethod
    def add_school_admin(cls, school_id, data):

        req: PrimaryContact = validator.validate_data(PrimaryContact, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        _school = School.GetSchool(school_id)

        _role: SchoolRole = SchoolRole.GetSchoolRole(req.role, _school.id)

        try:
            new_admin = User(email=req.email, msisdn=req.msisdn, password=None)
            db.session.add(new_admin)
            new_admin.save(refresh=True)

            add_school_admin = SchoolManager(
                school_id=_school.id,
                name=req.name,
                gender=req.gender,
                residence=req.address,
                user_id=new_admin.id
            )

            add_school_admin.school_roles = _role
            add_school_admin.save(refresh=True)
            Audit.add_audit('Added School Admin', current_user, add_school_admin.to_dict())
            return add_school_admin.to_dict()

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def update_school_admin(cls, user_id, school_id, data):
        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user_id, school_id)
        gender = data.get('gender')
        role = data.get('role')
        if role:
            _admin.school_role_id = role
        if gender:
            _admin.gender = gender
        _admin.update_table(data)
        Audit.add_audit('Updated School Admin Information', current_user, _admin.to_dict())
        return _admin.to_dict()

    @classmethod
    def reset_school_password(cls, user_id, school_id):
        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user_id, school_id)

        if not admin:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _admin.user
        Audit.add_audit('Reset School Admin password', current_user, _user.to_dict())
        return Helper.send_otp(_user)

    @classmethod
    def deactivate_school_user(cls, user_id, school_id, reason):
        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user_id, school_id)

        if not admin:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user: User = _admin.user
        Audit.add_audit('Changed School Admin account status', current_user, _user.to_dict())
        return Helper.disable_account(_user, reason)

    @classmethod
    def search_school_admin(cls, args, school_id):

        query = SchoolManager.query.join(User).filter(
            (SchoolManager.name.ilike(f'%{args}%'))
            | User.email.ilike(f'%{args}%')
        ).filter(SchoolManager.school_id == school_id)

        result = [x.to_dict() | x.user.to_dict() for x in query.all()]

        for item in result:
            item.pop("password", None)
            item.pop("id", None)

        return result or []

    @classmethod
    def get_user(cls, user_id, school_id):
        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user_id, school_id)
        return {
            **_admin.to_dict(),
            **_admin.user.as_dict(),
            "role_name": _admin.school_roles.name if _admin.school_roles else None,
            "permissions" : [x.name for x in _admin.school_roles.school_permissions] if _admin.school_roles else None
        }
