from application.utils.authenticator import authenticate
from application.Enums.Permission import PermissionEnum
from exceptions.codes import ExceptionCode
from exceptions.custom_exception import CustomException
from application.api.authAPI import auth_blueprint
from application.api.adminAPI import admin_blueprint
from application.api.rolePermissionAPI import roles_permission_blueprint
from application.api.schoolAPI import school_blueprint