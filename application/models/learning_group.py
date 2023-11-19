from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class LearningGroupTeachers(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    learning_group_id = db.Column(db.Integer, db.ForeignKey('learning_group.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)


class LearningGroupStudents(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    learning_group_id = db.Column(db.Integer, db.ForeignKey('learning_group.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)


class LearningGroupProjects(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    learning_group_id = db.Column(db.Integer, db.ForeignKey('learning_group.id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)


class LearningGroupComment(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    learning_group_id = db.Column(db.Integer, db.ForeignKey('learning_group.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    learning_groups = db.relationship("LearningGroup", back_populates="learning_group_comments")
    user = db.relationship("User", back_populates="learning_group_comments")


class LearningGroupFile(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    learning_group_id = db.Column(db.Integer, db.ForeignKey('learning_group.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_url = db.Column(db.Text, nullable=False)
    learning_groups = db.relationship("LearningGroup", back_populates="learning_group_files")
    user = db.relationship("User", back_populates="learning_group_files")


class LearningGroup(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True)
    description = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete='CASCADE'), nullable=False)
    schools = db.relationship("School", back_populates='learning_groups')
    user = db.relationship("User", back_populates='learning_groups')
    projects = db.relationship("Project", secondary='learning_group_projects', back_populates="learning_groups")
    students = db.relationship("Student", secondary='learning_group_students', back_populates="learning_groups")
    teachers = db.relationship("Teacher", secondary='learning_group_teachers', back_populates="learning_groups")

    learning_group_files = db.relationship("LearningGroupFile", back_populates="learning_groups", cascade="all, delete-orphan")
    learning_group_comments = db.relationship("LearningGroupComment", back_populates="learning_groups", cascade="all, delete-orphan")


    __table_args__ = (
        db.UniqueConstraint('school_id', 'name', name='uq_school_learning_group_name'),
    )

    @classmethod
    def GetLearningGroupName(cls, school_id, name):
        l_group = LearningGroup.query.filter_by(name=name, school_id=school_id).first()
        if not l_group:
            raise CustomException(message="Learning Group does not exist", status_code=404)
        return l_group

    @classmethod
    def GetLearningGroupID(cls, school_id, group_id):
        l_group = LearningGroup.query.filter_by(id=group_id, school_id=school_id).first()
        if not l_group:
            raise CustomException(message="Learning Group does not exist", status_code=404)
        return l_group
