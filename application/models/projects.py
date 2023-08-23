from sqlalchemy import JSON

from application import db
from application.Enums import Enums
from application.Mixins.GenericMixins import GenericMixin


class Project(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    description = db.Column(db.String(350), nullable=True)
    requirements = db.Column(db.JSON(none_as_null=True), nullable=True)
    documents = db.Column(db.JSON(none_as_null=True), nullable=True)
    reg_number = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=True)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    teachers = db.relationship("Teacher", back_populates='projects')
    students = db.relationship("Student", back_populates='projects')
    parents = db.relationship("Parent", back_populates='projects')
    schools = db.relationship("School",  back_populates='projects')
