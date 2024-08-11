import enum


class SubscriptionFeature(enum.Enum):
    # ROLES & PERMISSIONS
    ADD_ROLES = 'add_roles'
    ADD_LEARNING_GROUPS = 'add_learning_groups'
    MODIFY_LEARNING_GROUPS = 'update_learning_groups'
    ADD_SCHOOL_MANAGERS = 'add_school_manager'
