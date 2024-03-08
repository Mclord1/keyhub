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
            EmailHandler.welcome_mail(new_admin.email, add_school_admin.name)
            Audit.add_audit('Added School Admin', current_user, add_school_admin.to_dict())
            return add_school_admin.to_dict()

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def get_all_admin(cls, page, per_page, school_id):
        page = int(page)
        per_page = int(per_page)
        _admin = SchoolManager.query.filter_by(SchoolManager.school_id == school_id).order_by(
            desc(SchoolManager.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _admin.total
        results = [item for item in _admin.items]

        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_admins": len([x for x in results if x.user.isDeactivated]),
                "num_of_active_admins": len([x for x in results if not x.user.isDeactivated]),
                "num_of_admins": len(results),
                "admins": [{
                    **res.to_dict(),
                    "user_id": res.user.id,
                    **(res.user.as_dict() if res.user else {}),
                    "role_name": ' '.join(res.user.roles.name.split('_')) if res.user.roles else None
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_school_admin(cls, user_id, school_id, data):

        user: User = User.GetUser(user_id)

        if not user.managers:
            raise CustomException(message="School Admin does not exist", status_code=404)

        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user.managers.id, school_id)

        gender = data.get('gender')
        role = data.get('role')
        if role:
            _admin.school_role_id = role
        if gender:
            _admin.gender = gender
        _admin.update_table(data)
        Audit.add_audit('Updated School Admin Information', current_user, _admin.to_dict())
        return {**user.managers.to_dict(), "user_id": user.id}

    @classmethod
    def reset_school_password(cls, user_id, school_id):

        user: User = User.GetUser(user_id)

        if not user.managers:
            raise CustomException(message="School Admin does not exist", status_code=404)

        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user.managers.id, school_id)

        Audit.add_audit('Reset School Admin password', current_user, user.to_dict())
        return Helper.send_otp(user)

    @classmethod
    def deactivate_school_user(cls, user_id, school_id, reason):

        user: User = User.GetUser(user_id)

        if not user.managers:
            raise CustomException(message="School Admin does not exist", status_code=404)

        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user.managers.id, school_id)

        Audit.add_audit('Changed School Admin account status', current_user, user.to_dict())
        return Helper.disable_account(user, reason)

    @classmethod
    def search_school_admin(cls, args, school_id):

        query = SchoolManager.query.join(User).filter(
            (SchoolManager.name.ilike(f'%{args}%'))
            | User.email.ilike(f'%{args}%')
        ).filter(SchoolManager.school_id == school_id)

        result = []
        for manager in query.all():
            result_dict = {
                **manager.to_dict(),
                'email': manager.user.email,
                'user_id': manager.user.id,
                'msisdn': manager.user.msisdn,
                'isDeactivated': manager.user.isDeactivated,
                'deactivate_reason': manager.user.deactivate_reason,
            }
            result.append(result_dict)

        return result

    @classmethod
    def get_user(cls, user_id, school_id):

        user: User = User.GetUser(user_id)

        if not user.managers:
            raise CustomException(message="School Admin does not exist", status_code=404)

        _admin: SchoolManager = SchoolManager.GetSchoolAdmin(user.managers.id, school_id)

        return {
            **_admin.to_dict(),
            **_admin.user.as_dict(),
            "user_id": user.id,
            "role_name": _admin.school_roles.name if _admin.school_roles else None,
            "permissions": [x.name for x in _admin.school_roles.school_permissions] if _admin.school_roles else None
        }
