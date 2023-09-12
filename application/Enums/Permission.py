import enum


class PermissionEnum(enum.Enum):
    CREATE_SYSTEM_ADMIN = 'create_system_admin'
    CREATE_ROLES = 'create_roles'
    UPDATE_ADMIN = 'update_admin'
    VIEW_ADMIN = 'view_admin'
    DEACTIVATE_ADMIN = 'deactivate_admin'
    SEARCH_ADMIN = 'search_admin'
    ACCESS_ROLES = 'access_roles'
    MODIFY_ROLE = 'modify_role'
    CREATE_PERMISSIONS = 'create_permissions'
    DEACTIVATE_USER = 'deactivate_user'
    RESET_PASSWORD = 'reset_password'
    ADD_SCHOOL = 'add_school'
    LIST_SCHOOL = 'list_school'
    VIEW_SCHOOL_PROFILE = 'view_school_profile'
    DEACTIVATE_SCHOOL = 'deactivate_school'
    MODIFY_SCHOOL_PROFILE = 'modify_school_profile'
