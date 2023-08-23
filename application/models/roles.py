from application import db
from application.Mixins.GenericMixins import GenericMixin


class Role(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    user = db.relationship("User", secondary='user_role', back_populates='roles')
    permissions = db.relationship("Permission", secondary='role_permission', back_populates='roles')
