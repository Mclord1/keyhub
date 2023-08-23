from application import db
from application.Mixins.GenericMixins import GenericMixin


class SchoolTeacher(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)


class SchoolParent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)


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
    isDeactivated = db.Column(db.Boolean, default=True)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    managers = db.relationship("SchoolManager", back_populates='schools')
    subscriptions = db.relationship("Subscription", back_populates='schools')
    teachers = db.relationship("Teacher", secondary='school_teacher', back_populates='schools')
    students = db.relationship("Student", back_populates='schools')
    parents = db.relationship("Parent", secondary='school_parent', back_populates='schools')
    projects = db.relationship("Project", back_populates='schools')
    reports = db.relationship("Report", back_populates='schools')
