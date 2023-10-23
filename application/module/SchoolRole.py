from . import *


class SchoolRoleModel:

    @classmethod
    def get_school_roles(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _role = SchoolRole.query.filter(SchoolRole.school_id == school_id).order_by(
            desc(SchoolRole.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _role.total
        results = [item for item in _role.items]
        total_pages = (total_items - 1) // per_page + 1
        created_by = lambda x: User.query.filter_by(id=x).first()  # noqa

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": [
                {
                    **res.to_dict(add_filter=False),
                    "permissions": [x.to_dict() for x in res.permissions],
                    "created_by": created_by(res.admin_id).email if res.admin_id and created_by(res.admin_id) else None,
                    "creator_name": f'{created_by(res.admin_id).admins.first_name if created_by(res.admin_id) else None} {created_by(res.admin_id).admins.last_name if created_by(res.admin_id) else None}' if res.admin_id else None
                }
                for res in results
            ]
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_role_details(cls, role_id: int, school_id: int) -> dict:
        _role: SchoolRole = SchoolRole.GetRole(role_id, school_id)

        permissions = _role.permissions
        user_list = _role.schools.managers
        created_by: User = User.query.filter_by(id=_role.admin_id).first()
        return {
            'role_name': _role.name,
            'created_on': _role.created_at,
            'created_by': created_by.email if created_by else None,
            'creator_name': f'{created_by.admins.first_name} {created_by.admins.last_name}' if created_by else None,
            'country': created_by.admins.country if created_by else None,
            'users_assigned': len(user_list),
            'description': _role.description,
            'active': _role.active,
            'permissions': [x.to_dict() for x in permissions]
        }

    @classmethod
    def create_school_role(cls, role_name, description, school_id):
        _school = School.GetSchool(school_id)

        try:
            new_role = SchoolRole(name=role_name, admin_id=current_user.id, description=description, schools=_school)
            new_role.save(refresh=True)
            return new_role.to_dict()
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A role with the name already exist")

    @classmethod
    def delete_school_role(cls, role_id, school_id):
        _role: SchoolRole = SchoolRole.GetRole(role_id, school_id)

        if _role.schools:
            raise CustomException(message="There are schools associated to this school role", status_code=500)
        try:


            db.session.commit()
            db.session.delete(_role)
            db.session.commit()
            return "The role has been deleted"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def toggle_school_role_status(cls, role_id, school_id):
        _role: SchoolRole = SchoolRole.GetRole(role_id, school_id)

        try:
            _role.active = not _role.active
            db.session.commit()
            return f"The School active status has been changed to {_role.active}"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def update_school_role(cls, school_id, role_id, role_name, description):
        _role: SchoolRole = SchoolRole.GetRole(role_id, school_id)

        try:
            if role_name:
                _role.name = role_name
            if description:
                _role.description = description
            db.session.commit()
            return _role.to_dict()
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def assign_permission_to_school_role(cls, school_id, role_id, permission_id):

        if role_id is None or permission_id is None:
            raise CustomException("Both role_id and permission_id are required.", status_code=400)

        _role: SchoolRole = SchoolRole.GetRole(role_id, school_id)
        _permission: Permission = Permission.GetPermission(permission_id)

        if int(permission_id) in [x.id for x in _role.permissions]:
            raise CustomException(message="Permission already exist", status_code=400)

        try:

            _permission.school_roles.append(_role)
            db.session.commit()
            return f"The permission {_permission.name} has been assigned to {_role.name} role"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def remove_permission_from_school_role(cls, school_id, role_id, permission_id):
        _role: SchoolRole = SchoolRole.GetRole(role_id, school_id)
        _permission: Permission = Permission.GetPermission(permission_id)

        if _permission not in _role.permissions:
            raise CustomException(message="This permission doesn't exist on the role", status_code=404)
        try:


            _role.permissions.remove(_permission)
            db.session.commit()
            return {'permissions': [x.to_dict() for x in _role.permissions]}
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
