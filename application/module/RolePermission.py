from . import *


class RolePermission:

    @classmethod
    def GetAllRoles(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _role = Role.query.order_by(desc(Role.created_at)).paginate(page=page, per_page=per_page, error_out=False)
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
                    "permissions": [x.to_dict(add_filter=False) for x in res.permissions],
                    "created_by": created_by(res.admin_id).email if res.admin_id and created_by(res.admin_id) else None,
                    "creator_name": f'{created_by(res.admin_id).admins.first_name if created_by(res.admin_id) else None} {created_by(res.admin_id).admins.last_name if created_by(res.admin_id) else None}' if res.admin_id else None
                }
                for res in results if res.name not in [x.value for x in BasicRoles.__members__.values()]
            ]
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def GetAllPermissions(cls):
        _permissions = Permission.query.all()
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
            "school": [],
            "system_admin": [],
            "roles": [],
            "permissions": []
        }

        for _permission in _permissions:
            for category in permission_groups.keys():
                if category in _permission.name:
                    permission_groups[category].append(_permission.to_dict(add_filter=False))

        return permission_groups

    @classmethod
    def GetRoleDetails(cls, role_id: int) -> dict:
        _role: Role = Role.GetRole(role_id)

        permissions = _role.permissions
        user_list = _role.user
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
    def ToggleRoleActiveStatus(cls, role_id: int):
        _role: Role = Role.GetRole(role_id)

        try:
            _role.active = not _role.active
            db.session.commit()
            Audit.add_audit('Change Role status', current_user, _role.to_dict())
            return f"The Role active status has been changed to {_role.active}"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def AddRole(cls, role_name, description):
        try:
            new_role = Role(name=role_name, admin_id=current_user.id, description=description)
            new_role.save(refresh=True)
            Audit.add_audit('Add Role', current_user, new_role.to_dict())
            return new_role.to_dict(add_filter=False)
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A role with the name already exist")

    @classmethod
    def UpdateRole(cls, role_id, role_name, description):
        _role = Role.GetRole(role_id)
        try:
            _role.name = role_name
            _role.description = description
            db.session.commit()
            Audit.add_audit('Update Role Information', current_user, _role.to_dict())
            return _role.to_dict(add_filter=False)
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def DeleteRole(cls, role_id):

        _role = Role.GetRole(role_id)
        users_to_update = User.query.filter_by(role_id=role_id).all()

        if users_to_update:
            raise CustomException(message="There are users associated to this role", status_code=500)

        try:
            Audit.add_audit('Delete Role', current_user, _role.to_dict())
            db.session.commit()
            db.session.delete(_role)
            db.session.commit()
            return "The role has been deleted"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def AssignPermissionToRole(cls, role_id, permission_id):
        if role_id is None or permission_id is None:
            raise CustomException("Both role_id and permission_id are required.", status_code=400)

        _role = Role.GetRole(role_id)
        _permission: Permission = Permission.GetPermission(permission_id)

        if int(permission_id) in [x.id for x in _role.permissions]:
            raise CustomException(message="Permission already exist", status_code=400)
        try:

            _permission.roles.append(_role)
            db.session.commit()
            Audit.add_audit('Assign permission to Role', current_user, _role.to_dict())
            return f"The permission {_permission.name} has been assigned to {_role.name} role"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def RemovePermissionFromRole(cls, role_id, permission_id):
        _role: Role = Role.GetRole(role_id)
        _permission: Permission = Permission.GetPermission(permission_id)

        if _permission not in _role.permissions:
            raise CustomException(message="This permission doesn't exist on the role", status_code=404)
        try:
            Audit.add_audit('Remove permission from role', current_user, _role.to_dict())
            _role.permissions.remove(_permission)
            db.session.commit()
            return {'permissions': [x.to_dict(add_filter=False) for x in _role.permissions]}
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
