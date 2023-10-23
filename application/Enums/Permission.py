import enum


class PermissionEnum(enum.Enum):
    # ROLES & PERMISSIONS
    ADD_ROLES = 'add_roles'
    VIEW_ROLES = 'view_roles'
    MODIFY_ROLE = 'modify_role'
    DEACTIVATE_ROLE = 'delete_role'
    VIEW_PERMISSIONS = 'view_permissions'

    # ADMINS
    ADD_SYSTEM_ADMIN = 'add_system_admin'
    MODIFY_SYSTEM_ADMIN = 'update_system_admin'
    VIEW_SYSTEM_ADMIN = 'view_system_admin'
    DEACTIVATE_SYSTEM_ADMIN = 'deactivate_system_admin'
    RESET_SYSTEM_ADMIN_PASSWORD = 'reset_system_admin_password'

    # LEARNING GROUPS
    ADD_LEARNING_GROUPS = 'add_learning_groups'
    MODIFY_LEARNING_GROUPS = 'update_learning_groups'
    VIEW_LEARNING_GROUPS = 'view_learning_groups'
    DEACTIVATE_LEARNING_GROUPS = 'deactivate_learning_groups'

    # SCHOOL
    ADD_SCHOOL = 'add_school'
    VIEW_SCHOOL = 'view_school'
    DEACTIVATE_SCHOOL = 'deactivate_school'
    MODIFY_SCHOOL = 'modify_school'

    # SCHOOL MANAGER
    ADD_SCHOOL_MANAGERS = 'add_school_manager'
    VIEW_SCHOOL_MANAGERS = 'view_school_manager'
    DEACTIVATE_SCHOOL_MANAGERS = 'deactivate_school_manager'
    MODIFY_SCHOOL_MANAGERS = 'modify_school_manager'
    RESET_SCHOOL_MANAGERS_PASSWORD = 'reset_school_manager_password'

    # TEACHERS
    VIEW_TEACHERS = 'view_teacher'
    MODIFY_TEACHER = 'modify_teacher'
    ADD_TEACHER = 'add_teacher'
    DEACTIVATE_TEACHER = 'deactivate_teacher'
    RESET_TEACHER_PASSWORD = 'reset_teacher_password'

    # PARENTS
    VIEW_PARENTS = 'view_parents'
    MODIFY_PARENTS = 'modify_parents'
    ADD_PARENTS = 'add_parents'
    DEACTIVATE_PARENTS = 'deactivate_parents'
    RESET_PARENTS_PASSWORD = 'reset_parents_password'

    # STUDENTS
    VIEW_STUDENTS = 'view_students'
    MODIFY_STUDENTS = 'modify_students'
    ADD_STUDENTS = 'add_students'
    DEACTIVATE_STUDENTS = 'deactivate_students'
    RESET_STUDENT_PASSWORD = 'reset_student_password'

    # TRANSACTIONS
    VIEW_TRANSACTIONS = 'view_transactions'
    MODIFY_TRANSACTION = 'modify_transactions'
    ADD_TRANSACTION = 'add_transactions'
    DEACTIVATE_TRANSACTION = 'deactivate_transactions'

    # SUBSCRIPTIONS
    VIEW_SUBSCRIPTION = 'view_subscription'
    MODIFY_SUBSCRIPTION = 'modify_subscription'
    ADD_SUBSCRIPTION = 'add_subscription'
    DEACTIVATE_SUBSCRIPTION = 'deactivate_subscription'

    # PROJECTS
    VIEW_PROJECTS = 'view_projects'
    MODIFY_PROJECTS = 'modify_projects'
    ADD_PROJECTS = 'add_projects'
    DEACTIVATE_PROJECTS = 'deactivate_projects'
