from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class Student(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(350), nullable=True)
    last_name = db.Column(db.String(350), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship("User", back_populates='students')
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=True)
    _gender = db.Column(db.String(250), nullable=True)
    age = db.Column(db.String(250), nullable=True)
    dob = db.Column(db.String(250), nullable=True)
    country = db.Column(db.String(350), nullable=True)
    state = db.Column(db.String(350), nullable=True)
    address = db.Column(db.String(350), nullable=True)
    parents = db.relationship("Parent", back_populates='students')
    schools = db.relationship("School", back_populates='students')
    projects = db.relationship("Project", secondary='student_project', back_populates="students")
    learning_groups = db.relationship("LearningGroup", secondary='learning_group_students', back_populates="students")

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        # Ensure that the value is capitalized before assigning it
        self._gender = value.capitalize() if value else None

    @classmethod
    def GetStudent(cls, user_id):
        student = Student.query.filter_by(id=user_id).first()
        if not student:
            raise CustomException(message="Student does not exist", status_code=404)
        return student
