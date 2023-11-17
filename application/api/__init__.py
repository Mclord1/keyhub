from application.utils.authenticator import authenticate, has_school_privilege
from application.Enums.Permission import PermissionEnum
from exceptions.codes import ExceptionCode
from exceptions.custom_exception import CustomException
from application.api.authAPI import auth_blueprint
from application.api.adminAPI import admin_blueprint
from application.api.rolePermissionAPI import roles_permission_blueprint
from application.api.schoolAPI import school_blueprint
from application.api.teacherAPI import teacher_blueprint
from application.api.parentsAPI import parent_blueprint
from application.api.studentAPI import student_blueprint
from application.api.helperAPI import helper_blueprint
from application.api.subscriptionAPI import subcription_blueprint
from application.api.transactionAPI import transaction_blueprint
from application.api.auditAPI import audit_blueprint
from application.api.smeAPI import sme_bp
from application.api.keywordAPI import keywords_bp
from application.api.dashboardAPI import dashboard_blueprint