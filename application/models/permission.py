from application import db
from application.Mixins.GenericMixins import GenericMixin


class RolePermission(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)


class Permission(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship("Role", secondary='role_permission', back_populates='permissions')
