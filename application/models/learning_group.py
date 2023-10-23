from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class LearningGroupProjects(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    learning_group_id = db.Column(db.Integer, db.ForeignKey('learning_group.id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)
    teachers = db.relationship("Teacher", back_populates='learning_group_projects')
    students = db.relationship("Student", back_populates='learning_group_projects')
    projects = db.relationship("Project", back_populates='learning_group_projects')
    learning_group = db.relationship("LearningGroup", back_populates='learning_group_projects')


class LearningGroup(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True, unique=True)
    description = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete='CASCADE'), nullable=False)
    schools = db.relationship("School", back_populates='learning_group')
    user = db.relationship("User", back_populates='learning_group')
    learning_group_projects = db.relationship("LearningGroupProjects", back_populates='learning_group')

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
