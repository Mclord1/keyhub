from application import db
from application.Mixins.GenericMixins import GenericMixin


class TeacherStudent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)


class Teacher(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='teachers')
    address = db.Column(db.String(350), nullable=True)
    reg_number = db.Column(db.String(350), nullable=True, unique=True)
    isDeactivated = db.Column(db.Boolean, default=True)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    projects = db.relationship("Project", back_populates='teachers')
    students = db.relationship("Student", secondary='teacher_student', back_populates='teachers')
    schools = db.relationship("School", secondary='school_teacher', back_populates='teachers')
