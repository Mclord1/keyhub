from flask_jwt_extended import create_access_token, create_refresh_token

from . import *


class Authentication:
    @staticmethod
    def Login(email, password):
        user: User = User.query.filter_by(email=email).first()

        if user and user.isDeactivated:
            raise CustomException(ExceptionCode.ACCOUNT_ALREADY_DEACTIVATED)

        if user and user.password and bcrypt.checkpw(str(password).encode(), user.password.encode()):
            # Generate an access token
            access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=120))
            refresh_token = create_refresh_token(identity=user.id)
            role = user.roles[0]
            # Initialize an empty user_details dictionary
            user_details = {
                'role_name': ' '.join(str(role.name).split('_')) if role.name else None,
                'role_id': user.role_id
            }

            # Check and add user-related attributes if they are not None
            if user.parents:
                user_details.update(user.parents.to_dict())

            if user.teachers:
                user_details.update(user.teachers.to_dict())

            if user.students:
                user_details.update(user.students.to_dict())

            if user.admins:
                user_details.update(user.admins.to_dict())

            if user.managers:
                user_details.update(user.managers.to_dict())

            return return_json(
                OutputObj(message="Login successful",
                          data={"access_token": access_token,
                                "refresh_token": refresh_token,
                                'expiration_in_minutes': 120,
                                **user_details},
                          code=200)
            )

        else:
            raise CustomException(ExceptionCode.INVALID_CREDENTIALS)

    def changePassword(self):
        pass
