import bcrypt

from application import db
from application.Mixins.GenericMixins import GenericMixin
from application.models.messages import Message
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
    email = db.Column(db.String(250), nullable=True, unique=True)
    msisdn = db.Column(db.String(250), nullable=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="SET NULL"), nullable=True)
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
    projects = db.relationship("Project", back_populates='user')
    learning_groups = db.relationship("LearningGroup", back_populates='user')
    audits = db.relationship("Audit", back_populates='user')
    project_files = db.relationship("ProjectFile", back_populates="user", cascade="all, delete-orphan")
    project_comments = db.relationship("ProjectComment", back_populates="user", cascade="all, delete-orphan")
    student_files = db.relationship("StudentFile", back_populates="user", cascade="all, delete-orphan")
    student_comments = db.relationship("StudentComment", back_populates="user", cascade="all, delete-orphan")
    learning_group_files = db.relationship("LearningGroupFile", back_populates="user", cascade="all, delete-orphan")
    learning_group_comments = db.relationship("LearningGroupComment", back_populates="user", cascade="all, delete-orphan")
    subscribed_groups = db.relationship("LearningGroupSubscription", back_populates='user', cascade="all, delete-orphan")

    notifications = db.relationship("Notification", back_populates='user', cascade="all, delete-orphan")
    sent_messages = db.relationship('Message', foreign_keys=[Message.sender_id], back_populates='sender')
    received_messages = db.relationship('Message', foreign_keys=[Message.receiver_id], back_populates='receiver')

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
    def GetUserFullName(cls, user_id):
        user = User.query.filter_by(id=user_id).first()

        # Check and add user-related attributes if they are not None
        if user.parents:
            return f"{user.parents.first_name} {user.parents.last_name}"

        if user.teachers:
            return f"{user.teachers.first_name} {user.teachers.last_name}"

        if user.students:
            return f"{user.students.first_name} {user.students.last_name}"

        if user.admins:
            return f"{user.admins.first_name} {user.admins.last_name}"

        if user.managers:
            return f"{user.managers.name}"

    @classmethod
    def GetSchool(cls, user_id):
        user: User = User.query.filter_by(id=user_id).first()

        # Check and add user-related attributes if they are not None
        if user.parents:
            return user.parents.schools

        if user.teachers:
            return user.teachers.schools

        if user.students:
            return user.students.schools

        if user.managers:
            return user.managers.schools

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
