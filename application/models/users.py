import bcrypt

from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.codes import ExceptionCode
from exceptions.custom_exception import CustomException


class UserRole(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"),
                        nullable=True)  # Role name (e.g., 'parent', 'teacher', 'admin', etc.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    active = db.Column(db.Boolean, default=True)


class User(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    msisdn = db.Column(db.String(250), nullable=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=True)
    password = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=False)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    managers = db.relationship("SchoolManager", back_populates='user', uselist=False, cascade="all, delete-orphan")
    parents = db.relationship("Parent", back_populates='user', uselist=False, cascade="all, delete-orphan")
    students = db.relationship("Student", back_populates='user', uselist=False, cascade="all, delete-orphan")
    admins = db.relationship("Admin", back_populates='user', uselist=False, cascade="all, delete-orphan")
    teachers = db.relationship("Teacher", back_populates='user', uselist=False)
    roles = db.relationship('Role', back_populates='user', uselist=False)
    confirmation_codes = db.relationship('ConfirmationCode', back_populates='user', cascade="all, delete-orphan")
    subscription_plan = db.relationship("SubcriptionPlan", back_populates='user')

    def as_dict(self, include_sensitive_info=False):
        """
        Convert the User object to a dictionary representation,
        excluding sensitive information like password and id.
        """
        return {
            key: getattr(self, key)
            for key in ['email', 'msisdn', 'role_id', 'isDeactivated', 'deactivate_reason']
            if include_sensitive_info or key not in {'password', 'id'}
        }

    @classmethod
    def GetUser(cls, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise CustomException(message="User does not exist", status_code=404)
        return user

    @classmethod
    def CreateUser(cls, email, msisdn, role, password=None):
        try:
            user = User(email=email, msisdn=msisdn, password=password)
            user.roles = role
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            return user
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    def UpdatePassword(self, password):
        try:
            hash_value = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.password = hash_value.decode()
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    def UpdateMsisdn(self, msisdn):
        try:
            self.msisdn = msisdn
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
