from sqlalchemy import UniqueConstraint

from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


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
    learning_group_projects = db.relationship("LearningGroupProjects", back_populates='projects', cascade='all, delete')
    __table_args__ = (
        UniqueConstraint('school_id', 'name', name='uq_school_project_name'),
    )

    @classmethod
    def GetProject(cls, school_id, project_id):
        project = Project.query.filter_by(id=project_id, school_id=school_id).first()
        if not project:
            raise CustomException(message="Project does not exist", status_code=404)
        return project
