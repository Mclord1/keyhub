from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class StudentProject(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))


class TeacherProject(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))


class Project(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=False)
    description = db.Column(db.String(350), nullable=True)
    requirements = db.Column(db.JSON(none_as_null=True), nullable=True)
    documents = db.Column(db.JSON(none_as_null=True), nullable=True)
    reg_number = db.Column(db.String(350), nullable=True)
    isDeactivated = db.Column(db.Boolean, default=False)
    deactivate_reason = db.Column(db.String(450), nullable=True)
    schools = db.relationship("School", back_populates='projects')
    user = db.relationship("User", back_populates='projects')
    students = db.relationship("Student", secondary='student_project', back_populates="projects")
    teachers = db.relationship("Teacher", secondary='teacher_project', back_populates="projects")
    learning_groups = db.relationship("LearningGroup", secondary='learning_group_projects', back_populates="projects")

    __table_args__ = (
        db.UniqueConstraint('school_id', 'name', name='uq_school_project_name'),
    )

    @classmethod
    def GetProject(cls, school_id, project_id):
        project = Project.query.filter_by(id=project_id, school_id=school_id).first()
        if not project:
            raise CustomException(message="Project does not exist", status_code=404)
        return project
