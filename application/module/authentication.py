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
            user_details = {
                'role_name': None,
                'role_id': None
            }

            if user.roles:
                role = user.roles

                # Initialize an empty user_details dictionary
                user_details.update({
                    'role_name': ' '.join(str(role.name).split('_')) if role.name else None,
                    'role_id': user.role_id,
                    **user.as_dict()
                })

            if user.managers and user.managers.school_roles:
                role = user.managers.school_roles

                user_details.update({
                    'role_name': ' '.join(str(role.name).split('_')) if role.name else None,
                    'role_id': user.managers.school_role_id,
                    **user.as_dict()
                })

            # Check and add user-related attributes if they are not None
            if user.parents:
                user_details.update({**user.parents.to_dict(), "school_id": [x.id for x in user.parents.schools]})

            if user.teachers:
                user_details.update({**user.teachers.to_dict(), "school_id": [x.id for x in user.teachers.schools]})

            if user.students:
                user_details.update({**user.students.to_dict(), "school_id": user.students.school_id})

            if user.admins:
                user_details.update(user.admins.to_dict())

            if user.managers:
                user_details.update(
                    {
                        **user.managers.to_dict(),
                        "school_id": user.managers.school_id
                    })

            return return_json(
                OutputObj(message="Login successful", data={"access_token": access_token, "refresh_token": refresh_token, 'expiration_in_minutes': 120, **user_details}, code=200)
            )

        else:
            raise CustomException(ExceptionCode.INVALID_CREDENTIALS)

    @staticmethod
    def update_password(code: str, password):
        _user: User = User.GetUser(current_user.id)
        confirm_code: ConfirmationCode = ConfirmationCode.query.filter(ConfirmationCode.code == code, ConfirmationCode.user_id == current_user.id).first()
        current_time = datetime.datetime.now()

        if not confirm_code:
            raise CustomException(message="Invalid confirmation code", status_code=400)

        if current_time > confirm_code.expiration:
            raise CustomException(message="OTP code has already expired", status_code=400)

        _user.UpdatePassword(password)

        return return_json(OutputObj(message="Password has been set successfully. Please login again.", code=200))

    @staticmethod
    def set_up_password(email, password):

        _user: User = User.query.filter_by(email=email).first()

        if not _user:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        _user.UpdatePassword(password)

        return return_json(OutputObj(message="Password has been set successfully.", code=200))
