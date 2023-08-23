from application import db
from application.Mixins.GenericMixins import GenericMixin


class Student(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='students')
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    address = db.Column(db.String(350), nullable=True)
    residential_address = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=True)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    projects = db.relationship("Project", back_populates='students')
    parents = db.relationship("Parent", back_populates='students')
    schools = db.relationship("School",  back_populates='students')
    teachers = db.relationship("Teacher", secondary='teacher_student', back_populates='students')
