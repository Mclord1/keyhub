import datetime
import random
import string

from application import db
from application.models import ConfirmationCode, User
from exceptions.custom_exception import CustomException


class Helper:

    @classmethod
    def generate_token(cls):
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def send_otp(cls, user):
        otp_code = cls.generate_token()
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
        add_to_confirmation = ConfirmationCode(email=user.email, user_id=user.id, code=otp_code,
                                               expiration=expiration_time)
        add_to_confirmation.save(refresh=True)
        # TODO :: Send OTP to users email or phone_number
        return f"OTP code has been sent to {user.email}"

    @classmethod
    def look_up_account(cls, Model, User, args):
        query = Model.query.join(User).filter(
            (Model.first_name.ilike(f'%{args}%') | Model.last_name.ilike(f'%{args}%'))
            | User.email.ilike(f'%{args}%')
        )
        result = [x.to_dict() | x.user.to_dict() for x in query.all()]

        for item in result:
            item.pop("password", None)
            item.pop("id", None)

        return result or []

    @classmethod
    def disable_account(cls, user, reason):
        if user.isDeactivated:
            raise CustomException(message="User account has already been deactivated", status_code=400)

        user.isDeactivated = True
        user.deactivate_reason = reason
        db.session.commit()
        return f"{user.email} account has been deactivated"

    @classmethod
    def User_Email_OR_Msisdn_Exist(cls, email, msisdn):
        user: User = db.session.query(User).filter(
            (User.email == email) or (User.msisdn == msisdn)
        ).first()

        if user:
            raise CustomException(
                message="The Email or Phone number already registered with other user.",
                status_code=400
            )

        return True
