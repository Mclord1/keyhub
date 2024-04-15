from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class StudentComment(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    students = db.relationship("Student", back_populates="student_comments")
    user = db.relationship("User", back_populates="student_comments")


class StudentFile(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_url = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.Text, nullable=True)
    students = db.relationship("Student", back_populates="student_files")
    user = db.relationship("User", back_populates="student_files")


class StudentParent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))


class Student(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(350), nullable=True)
    last_name = db.Column(db.String(350), nullable=True)
    profile_image = db.Column(db.Text, nullable=True)
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

    middle_name = db.Column(db.String(350), nullable=True)
    nick_name = db.Column(db.String(350), nullable=True)
    current_school = db.Column(db.String(350), nullable=True)
    parent_name = db.Column(db.String(350), nullable=True)
    parent_email = db.Column(db.String(350), nullable=True)
    how_you_knew_about_us = db.Column(db.String(350), nullable=True)
    why_use_us = db.Column(db.String(350), nullable=True)
    interest = db.Column(db.Text, nullable=True)
    msisdn = db.Column(db.String(350), nullable=True)
    parent_msisdn = db.Column(db.String(350), nullable=True)
    father_name = db.Column(db.String(350), nullable=True)
    father_msisdn = db.Column(db.String(350), nullable=True)
    father_address = db.Column(db.String(350), nullable=True)
    father_email = db.Column(db.String(350), nullable=True)
    mother_name = db.Column(db.String(350), nullable=True)
    mother_msisdn = db.Column(db.String(350), nullable=True)
    mother_address = db.Column(db.String(350), nullable=True)
    mother_email = db.Column(db.String(350), nullable=True)
    any_medical_condition = db.Column(db.Boolean, default=False, nullable=True)
    medical_condition = db.Column(db.Text, nullable=True)
    any_educational_needs = db.Column(db.Boolean, default=False, nullable=True)
    educational_needs = db.Column(db.Text, nullable=True)
    any_learning_delay = db.Column(db.Boolean, default=False, nullable=True)
    learning_delay = db.Column(db.Text, nullable=True)
    emergency_contact_first_name = db.Column(db.String(350), nullable=True)
    emergency_contact_last_name = db.Column(db.String(350), nullable=True)
    emergency_contact_msisdn = db.Column(db.String(350), nullable=True)
    emergency_contact_relationship = db.Column(db.String(350), nullable=True)

    any_allergies = db.Column(db.Boolean, default=False, nullable=True)
    allergies = db.Column(db.Text, nullable=True)

    any_special_dietary = db.Column(db.Boolean, default=False, nullable=True)
    special_dietary = db.Column(db.Text, nullable=True)

    has_siblings = db.Column(db.Boolean, default=False, nullable=True)

    more_details_about_student = db.Column(db.Text, nullable=True)

    parents = db.relationship("Parent", secondary='student_parent', back_populates='students')
    schools = db.relationship("School", back_populates='students')
    teachers = db.relationship("Teacher", secondary='teacher_student', back_populates='students')
    projects = db.relationship("Project", secondary='student_project', back_populates="students")
    learning_groups = db.relationship("LearningGroup", secondary='learning_group_students', back_populates="students")
    student_files = db.relationship("StudentFile", back_populates="students", cascade="all, delete-orphan")
    student_comments = db.relationship("StudentComment", back_populates="students", cascade="all, delete-orphan")

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

    @classmethod
    def GetSchoolStudent(cls, user_id, school_id):
        student = Student.query.filter_by(id=user_id, school_id=school_id).first()
        if not student:
            raise CustomException(message="Student does not exist", status_code=404)
        return student
