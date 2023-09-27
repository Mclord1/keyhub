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
            access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=60))
            refresh_token = create_refresh_token(identity=user.id)
            role = user.roles[0]
            user_details = {**user.to_dict(), 'role_name': ' '.join(str(role.name).split('_')) if role.name else None}

            user_details.pop('password')
            return return_json(
                OutputObj(message="Login successful", data={"access_token": access_token, "refresh_token": refresh_token, 'expiration_in_minutes': 60, **user_details}, code=200))

        else:
            raise CustomException(ExceptionCode.INVALID_CREDENTIALS)

    def changePassword(self):
        pass
