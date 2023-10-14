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
        created_by = lambda x: User.query.filter_by(id=x).first()

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": [
                {
                    **res.to_dict(add_filter=False),
                    "created_by": created_by(res.admin_id).email if res.admin_id else None,
                    "creator_name": f'{created_by(res.admin_id).admins.first_name} {created_by(res.admin_id).admins.last_name}' if res.admin_id else None
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
                    permission_groups[category].append(_permission.to_dict())

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
            'permissions': [x.to_dict() for x in permissions]
        }

    @classmethod
    def ToggleRoleActiveStatus(cls, role_id: int, status: bool):
        _role: Role = Role.GetRole(role_id)
        _role.active = status
        db.session.commit()
        return f"The Role active status has been changed to {status}"

    @classmethod
    def AddRole(cls, role_name, description):
        try:
            new_role = Role(name=role_name, admin_id=current_user.id, description=description)
            new_role.save(refresh=True)
            return new_role.to_dict()
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A role with the name already exist")

    @classmethod
    def UpdateRole(cls, role_id, role_name, description):
        _role = Role.GetRole(role_id)
        _role.name = role_name
        _role.description = description
        db.session.commit()
        return _role.to_dict()

    @classmethod
    def DeleteRole(cls, role_id):
        _role = Role.GetRole(role_id)
        users_to_update = User.query.filter_by(role_id=role_id).all()
        for user in users_to_update:
            user.role_id = None
        db.session.commit()
        db.session.delete(_role)
        db.session.commit()
        return "The role has been deleted"

    @classmethod
    def AssignPermissionToRole(cls, role_id, permission_id):

        if role_id is None or permission_id is None:
            raise CustomException("Both role_id and permission_id are required.", status_code=400)

        _role = Role.GetRole(role_id)
        _permission: Permission = Permission.GetPermission(permission_id)

        if int(permission_id) in [x.id for x in _role.permissions]:
            raise CustomException(message="Permission already exist", status_code=400)

        _permission.roles.append(_role)
        db.session.commit()
        return f"The permission {_permission.name} has been assigned to {_role.name} role"

    @classmethod
    def RemovePermissionFromRole(cls, role_id, permission_id):
        _role: Role = Role.GetRole(role_id)
        _permission: Permission = Permission.GetPermission(permission_id)

        if _permission not in _role.permissions:
            raise CustomException(message="This permission doesn't exist on the role", status_code=404)

        _role.permissions.remove(_permission)
        db.session.commit()
        return {'permissions': [x.to_dict() for x in _role.permissions]}
