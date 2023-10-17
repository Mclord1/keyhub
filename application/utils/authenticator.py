from functools import wraps

import jwt
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_current_user
from application import db
from application.Enums.Enums import BasicRoles
from exceptions.custom_exception import CustomException, ExceptionCode


def authenticate(permission_name='Not-Set'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user = get_current_user()

                if user.isDeactivated:
                    raise CustomException(message="Your account has been deactivated", status_code=400)

                # Check if the user's role has the required permission if permission is provided
                if permission_name != 'Not-Set':
                    if permission_name.value in [permission.name for permission in user.roles.permissions if permission.active]:
                        func_response = f(*args, **kwargs)
                        db.session.close()
                        return func_response
                    else:
                        raise CustomException(ExceptionCode.PERMISSION_DENIED)

            except jwt.ExpiredSignatureError:
                raise CustomException(ExceptionCode.EXPIRED_TOKEN)
            except jwt.InvalidTokenError:
                raise CustomException(ExceptionCode.INVALID_TOKEN)

        return decorated_function

    return decorator


def has_school_privilege(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        school_id = int(request.view_args.get('school_id'))
        if not school_id:
            raise CustomException(message="School Id param must be passed in the URL", status_code=400)
        if user.roles and BasicRoles.SYSTEM_ADMIN != user.roles.name:

            if not user.managers:
                raise CustomException(message="only Admin or school manager has privilege.", status_code=401)

            if user.managers and user.managers.schools.id != school_id:
                raise CustomException(message="You don't have access to this school", status_code=401)
        return f(*args, **kwargs)

    return decorated_func
