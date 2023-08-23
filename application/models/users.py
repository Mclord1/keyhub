import enum
from application import db
from application.Mixins.GenericMixins import GenericMixin


class UserRole(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)  # Role name (e.g., 'parent', 'teacher', 'admin', etc.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    active = db.Column(db.Boolean, default=True)


class User(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    msisdn = db.Column(db.String(250), nullable=True, unique=True)
    password = db.Column(db.String(350), nullable=True)
    managers = db.relationship("SchoolManager", back_populates='user')
    parents = db.relationship("Parent", back_populates='user')
    students = db.relationship("Student", back_populates='user')
    admins = db.relationship("Admin", back_populates='user')
    teachers = db.relationship("Teacher", back_populates='user')
    roles = db.relationship('Role', secondary='user_role', back_populates='user')
