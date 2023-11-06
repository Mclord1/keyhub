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
                    "permissions": [x.to_dict(add_filter=False) for x in res.school_permissions],
                    "created_by": created_by(res.admin_id).email if res.admin_id and created_by(res.admin_id) else None,
                    "creator_name": f'{created_by(res.admin_id).admins.first_name if created_by(res.admin_id) else None} {created_by(res.admin_id).admins.last_name if created_by(res.admin_id) else None}' if res.admin_id else None
                }
                for res in results
            ]
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_role_details(cls, role_id: int, school_id: int) -> dict:
        _role: SchoolRole = SchoolRole.GetSchoolRole(role_id, school_id)

        permissions = _role.school_permissions
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
            'permissions': [x.to_dict(add_filter=False) for x in permissions]
        }

    @classmethod
    def GetAllPermissions(cls):
        _permissions = SchoolPermission.query.all()
        if not _permissions:
            return []

        permission_groups = {
            "students": [],
            "projects": [],
            "subscription": [],
            "transactions": [],
            "parents": [],
            "teacher": [],
            "school_manager": [],
            "roles": [],
            "permissions": [],
            "learning_groups": [],
            "sme": []
        }

        for _permission in _permissions:
            for category in permission_groups.keys():
                if category in _permission.name:
                    permission_groups[category].append(_permission.to_dict(add_filter=False))

        return permission_groups

    @classmethod
    def create_school_role(cls, role_name, description, school_id):
        _school = School.GetSchool(school_id)

        try:
            new_role = SchoolRole(name=role_name, admin_id=current_user.id, description=description, schools=_school)
            new_role.save(refresh=True)
            Audit.add_audit('Add School Role', current_user, new_role.to_dict(add_filter=False))
            return new_role.to_dict(add_filter=False)
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A role with the name already exist")

    @classmethod
    def delete_school_role(cls, role_id, school_id):
        _role: SchoolRole = SchoolRole.GetSchoolRole(role_id, school_id)
        if _role.managers:
            raise CustomException(message="There are schools managers associated to this school role", status_code=500)
        try:
            Audit.add_audit('Delete School Role', current_user, _role.to_dict(add_filter=False))
            db.session.commit()
            db.session.delete(_role)
            db.session.commit()
            return "The role has been deleted"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def toggle_school_role_status(cls, role_id, school_id):
        _role: SchoolRole = SchoolRole.GetSchoolRole(role_id, school_id)
        try:
            _role.active = not _role.active
            db.session.commit()
            Audit.add_audit('Deactivate School Role' if not _role.active else 'Activate School Role', current_user, _role.to_dict(add_filter=False))
            return f"The School active status has been changed to {_role.active}"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def update_school_role(cls, school_id, role_id, role_name, description):
        _role: SchoolRole = SchoolRole.GetSchoolRole(role_id, school_id)

        try:
            if role_name:
                _role.name = role_name
            if description:
                _role.description = description
            db.session.commit()
            Audit.add_audit('Update School Role Information', current_user, _role.to_dict(add_filter=False))
            return _role.to_dict(add_filter=False)
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def assign_permission_to_school_role(cls, school_id, role_id, permission_id):

        if role_id is None or permission_id is None:
            raise CustomException("Both role_id and School permission_id are required.", status_code=400)

        _role: SchoolRole = SchoolRole.GetSchoolRole(role_id, school_id)
        _permission: SchoolPermission = SchoolPermission.GetPermission(permission_id)

        if int(permission_id) in [x.id for x in _role.school_permissions]:
            raise CustomException(message="School Permission already exist", status_code=400)

        try:

            _permission.school_roles.append(_role)
            db.session.commit()
            Audit.add_audit('Assign Permission to School Role Information', current_user, _role.to_dict(add_filter=False))
            return f"The School permission {_permission.name} has been assigned to {_role.name} role"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def remove_permission_from_school_role(cls, school_id, role_id, permission_id):
        _role: SchoolRole = SchoolRole.GetSchoolRole(role_id, school_id)
        _permission: SchoolPermission = SchoolPermission.GetPermission(permission_id)

        if _permission not in _role.school_permissions:
            raise CustomException(message="This School permission doesn't exist on the role", status_code=404)
        try:

            _role.school_permissions.remove(_permission)
            db.session.commit()
            Audit.add_audit('Remove Permission from School Role Information', current_user, _role.to_dict(add_filter=False))
            return {'permissions': [x.to_dict(add_filter=False) for x in _role.school_permissions]}
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
