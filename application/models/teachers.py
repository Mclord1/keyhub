from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class TeacherStudent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)


class Teacher(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(350), nullable=True)
    last_name = db.Column(db.String(350), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='teachers')
    _gender = db.Column(db.String(250), nullable=True)
    country = db.Column(db.String(350), nullable=True)
    state = db.Column(db.String(350), nullable=True)
    address = db.Column(db.String(350), nullable=True)
    reg_number = db.Column(db.String(350), nullable=True, unique=True)
    projects = db.relationship("Project", back_populates='teachers')
    students = db.relationship("Student", secondary='teacher_student', back_populates='teachers')
    schools = db.relationship("School", secondary='school_teacher', back_populates='teachers')

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        # Ensure that the value is capitalized before assigning it
        self._gender = value.capitalize() if value else None

    @classmethod
    def GetTeacher(cls, user_id):
        teacher = Teacher.query.filter_by(id=user_id).first()
        if not teacher:
            raise CustomException(message="Teacher does not exist", status_code=404)
        return teacher
