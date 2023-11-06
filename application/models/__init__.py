from application.models.admin import Admin
from application.models.audit import Audit
from application.models.confirmation_code import ConfirmationCode
from application.models.country import Country
from application.models.learning_group import LearningGroupTeachers, LearningGroupStudents, LearningGroupProjects, LearningGroup
from application.models.parents import Parent
from application.models.permission import RolePermission, Permission
from application.models.permission import RolePermission, Permission, SchoolPermission
from application.models.projects import Project, TeacherProject, StudentProject, ProjectActivity
from application.models.reports import Report
from application.models.roles import Role
from application.models.school_manager import SchoolManager
from application.models.schools import SchoolRole, School, SchoolTeacher, SchoolParent, SchoolRolePermission
from application.models.smeModel import SME, Keywords
from application.models.state import State
from application.models.students import Student
from application.models.subscription import Subscription, SubcriptionPlan
from application.models.teachers import Teacher, TeacherStudent
from application.models.users import User, UserRole
from application.models.transactions import Transaction

