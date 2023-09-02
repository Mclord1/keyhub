import enum

import bcrypt

from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class UserRole(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)  # Role name (e.g., 'parent', 'teacher', 'admin', etc.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    active = db.Column(db.Boolean, default=True)


class User(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    msisdn = db.Column(db.String(250), nullable=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    password = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=False)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    managers = db.relationship("SchoolManager", back_populates='user', uselist=False)
    parents = db.relationship("Parent", back_populates='user', uselist=False)
    students = db.relationship("Student", back_populates='user', uselist=False)
    admins = db.relationship("Admin", back_populates='user', uselist=False)
    teachers = db.relationship("Teacher", back_populates='user', uselist=False)
    roles = db.relationship('Role', back_populates='user', uselist=True)
    confirmation_codes = db.relationship('ConfirmationCode', back_populates='user')

    @classmethod
    def GetUser(cls, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise CustomException(message="User does not exist")
        return user

    @classmethod
    def CreateUser(cls, email, msisdn, role):
        user = User(email=email, msisdn=msisdn)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

    def UpdatePassword(self, password):
        hash_value = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.password = hash_value.decode()
        db.session.commit()

    def UpdateMsisdn(self, msisdn):
        self.msisdn = msisdn
        db.session.commit()
