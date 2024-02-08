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


class ProjectActivity(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    finish_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    learning_objectives = db.Column(db.Text, nullable=True)
    resources = db.Column(db.Text, nullable=True)
    supporting_weblinks = db.Column(db.String(350), nullable=True)
    supporting_media = db.Column(db.String(350), nullable=True)
    ways_to_extend = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum( 'open', 'completed', name='status'), nullable=True, default='open')
    projects = db.relationship("Project", back_populates="activities")


class ProjectComment(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    projects = db.relationship("Project", back_populates="project_comments")
    user = db.relationship("User", back_populates="project_comments")


class ProjectFile(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    file_name = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_url = db.Column(db.Text, nullable=False)
    projects = db.relationship("Project", back_populates="project_files")
    user = db.relationship("User", back_populates="project_files")


class ChecklistQuestion(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='SET NULL'))
    admins = db.relationship("Admin", back_populates="checklist")


class Project(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=False)
    reg_number = db.Column(db.String(350), nullable=True)

    requirements = db.Column(db.JSON(none_as_null=True), nullable=True)
    lead_teacher = db.Column(db.Integer, nullable=True)
    supporting_teachers = db.Column(db.Text, nullable=True)
    documents = db.Column(db.JSON(none_as_null=True), nullable=True)
    description = db.Column(db.Text, nullable=True)
    academic_year = db.Column(db.String(350), nullable=True)
    term = db.Column(db.Text, nullable=True)
    project_type = db.Column(db.String(350), nullable=True)
    age_group = db.Column(db.String(350), nullable=True)
    key_words = db.Column(db.JSON(none_as_null=True), nullable=True)
    project_aim = db.Column(db.Text, nullable=True)
    problem_to_solve = db.Column(db.JSON(none_as_null=True), nullable=True)
    weblinks = db.Column(db.Text, nullable=True)
    milestones = db.Column(db.Text, nullable=True)
    final_product = db.Column(db.JSON(none_as_null=True), nullable=True)
    learning_goals = db.Column(db.JSON(none_as_null=True), nullable=True)
    subject_matter = db.Column(db.JSON(none_as_null=True), nullable=True)
    meets_project_duration = db.Column(db.Text, nullable=True)
    curriculum = db.Column(db.Text, nullable=True)

    project_checklist = db.Column(db.JSON(none_as_null=True), nullable=True)
    is_private = db.Column(db.Boolean, default=False)
    project_duration = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, default='pending')
    isDeactivated = db.Column(db.Boolean, default=False)
    deactivate_reason = db.Column(db.Text, nullable=True)
    schools = db.relationship("School", back_populates='projects')
    user = db.relationship("User", back_populates='projects')
    students = db.relationship("Student", secondary='student_project', back_populates="projects")
    teachers = db.relationship("Teacher", secondary='teacher_project', back_populates="projects")
    learning_groups = db.relationship("LearningGroup", secondary='learning_group_projects', back_populates="projects")
    activities = db.relationship("ProjectActivity", back_populates="projects", cascade="all, delete-orphan")
    project_files = db.relationship("ProjectFile", back_populates="projects", cascade="all, delete-orphan")
    project_comments = db.relationship("ProjectComment", back_populates="projects", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint('school_id', 'name', name='uq_school_project_name'),
    )

    @classmethod
    def GetProject(cls, school_id, project_id):
        project = Project.query.filter_by(id=project_id, school_id=school_id).first()
        if not project:
            raise CustomException(message="Project does not exist", status_code=404)
        return project
