from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class Role(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True, unique=True)
    admin_id = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(1000), nullable=True)
    user = db.relationship("User", secondary='user_role', back_populates='roles', cascade="all, delete")
    permissions = db.relationship("Permission", secondary='role_permission', back_populates='roles', cascade="all, delete")

    @staticmethod
    def GetRole(id):
        role = Role.query.filter_by(id=id).first()
        if not role:
            raise CustomException(message="The provided role does not exist")
        return role

    @staticmethod
    def GetRoleByName(name):
        role = Role.query.filter_by(name=name).first()
        if not role:
            raise CustomException(message="The provided role does not exist")
        return role
