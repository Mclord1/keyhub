from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class SchoolTeacher(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete="CASCADE"), nullable=True)


class SchoolParent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id', ondelete="CASCADE"), nullable=True)


class SchoolRole(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    admin_id = db.Column(db.Integer, nullable=True)
    school_id = db.Column(db.ForeignKey('school.id', ondelete='CASCADE'), nullable=True)
    active = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(1000), nullable=True)
    school_permissions = db.relationship("SchoolPermission", secondary='school_role_permission', back_populates='school_roles', cascade="all, delete")
    schools = db.relationship("School", back_populates='school_roles')
    managers = db.relationship("SchoolManager", back_populates='school_roles',  passive_deletes=True)

    __table_args__ = (
        db.UniqueConstraint('school_id', 'name', name='uq_school_role_name'),
    )

    @staticmethod
    def GetSchoolRole(id, school_id):
        role = SchoolRole.query.filter_by(id=id, school_id=school_id).first()
        if not role:
            raise CustomException(message="The provided role does not exist")
        return role


class SchoolRolePermission(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_permission_id = db.Column(db.Integer, db.ForeignKey('school_permission.id', ondelete="CASCADE"), nullable=True)
    school_role_id = db.Column(db.Integer, db.ForeignKey('school_role.id', ondelete="CASCADE"), nullable=True)


class School(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True, unique=True)
    address = db.Column(db.String(350), nullable=True)
    url = db.Column(db.String(350), nullable=True)
    email = db.Column(db.String(350), nullable=True, unique=True)
    msisdn = db.Column(db.String(350), nullable=True, unique=True)
    reg_number = db.Column(db.String(350), nullable=True, unique=True)
    country = db.Column(db.String(350), nullable=True)
    state = db.Column(db.String(350), nullable=True)
    logo = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=False)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    managers = db.relationship("SchoolManager", back_populates='schools', cascade="all, delete-orphan")
    subscriptions = db.relationship("Subscription", back_populates='schools', cascade="all, delete-orphan")
    teachers = db.relationship("Teacher", secondary='school_teacher', back_populates='schools', cascade="all, delete")
    students = db.relationship("Student", back_populates='schools', cascade="all, delete-orphan", single_parent=True)
    parents = db.relationship("Parent", secondary='school_parent', back_populates='schools', cascade="all, delete")
    projects = db.relationship("Project", back_populates='schools', cascade="all, delete-orphan")
    reports = db.relationship("Report", back_populates='schools', cascade="all, delete-orphan")
    school_roles = db.relationship("SchoolRole", back_populates='schools')
    learning_groups = db.relationship("LearningGroup", back_populates='schools', cascade="all, delete-orphan")

    @classmethod
    def GetSchool(cls, school_id):
        user = School.query.filter_by(id=school_id).first()
        if not user:
            raise CustomException(message="School does not exist", status_code=404)
        return user
