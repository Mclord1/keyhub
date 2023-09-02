from functools import wraps

import jwt
from flask_jwt_extended import verify_jwt_in_request, get_current_user

from exceptions.custom_exception import CustomException, ExceptionCode


def authenticate(permission_name=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user = get_current_user()

                if user.isDeactivated:
                    raise CustomException(message="Your account has been deactivated", status_code=400)

                # Check if the user's role has the required permission if permission is provided
                if permission_name:
                    if permission_name.value in [permission.name for role in user.roles for permission in role.permissions if permission.active]:
                        return f(*args, **kwargs)
                    else:
                        raise CustomException(ExceptionCode.PERMISSION_DENIED)

            except jwt.ExpiredSignatureError:
                raise CustomException(ExceptionCode.EXPIRED_TOKEN)
            except jwt.InvalidTokenError:
                raise CustomException(ExceptionCode.INVALID_TOKEN)

        return decorated_function

    return decorator

