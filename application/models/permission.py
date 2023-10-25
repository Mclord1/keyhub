from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class RolePermission(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id', ondelete="CASCADE"), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=True)


class Permission(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True, unique=True)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship("Role", secondary='role_permission', back_populates='permissions', passive_deletes=True)

    @staticmethod
    def GetPermission(id):
        permission = Permission.query.filter_by(id=id).first()
        if not permission:
            raise CustomException(message="The provided permission does not exist")
        return permission


class SchoolPermission(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True, unique=True)
    active = db.Column(db.Boolean, default=True)
    school_roles = db.relationship("SchoolRole", secondary='school_role_permission', back_populates='school_permissions', passive_deletes=True)

    @staticmethod
    def GetPermission(id):
        permission = SchoolPermission.query.filter_by(id=id).first()
        if not permission:
            raise CustomException(message="The provided permission does not exist")
        return permission
