from traceback import print_exc

import bcrypt
import boto3
import jsonschema
from marshmallow import (
    ValidationError,
    validates,
)
from sqlalchemy import func, JSON, BigInteger

from app import db
from app.Enums.Enums import *
from app.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException, ExceptionCode


# from submodule_util_3kle.util.get_cognito_client import CLIENT_ID, USER_POOL_ID


class User(GenericMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # uuid
    email = db.Column(db.String(250), unique=True)
    first_name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.Enum(GenderEnums, values_callable=lambda x: [str(member.value) for member in GenderEnums]), nullable=True)
    date_of_birth = db.Column(db.String(10))
    phone_number = db.Column(db.String(20), unique=True)
    panic_balance = db.Column(JSON, default={
        "panic_amount": 0,
        "panic_balance": False
    })
    image_id = db.Column(db.String(400), unique=True)
    address = db.Column(db.String(350), nullable=True)
    city = db.Column(db.String(350), nullable=True)
    lga = db.Column(db.String(350), nullable=True)
    state = db.Column(db.String(350), nullable=True)
    country = db.Column(db.String(350), nullable=True)
    currency = db.Column(db.String(50), default='NGN')
    base_currency = db.Column(db.String(50), default='NGN')

    country_code = db.Column(db.String(50), nullable=True)
    bvn = db.Column(db.String(11), nullable=True)
    user_account_tier = db.Column(db.Enum(AccountTierEnum, nullable=True, values_callable=lambda x: [str(member.value) for member in AccountTierEnum]))
    pin = db.Column(db.String(550), nullable=True)
    pin_verified_on = db.Column(BigInteger, nullable=True)
    is_spend_plus_save_enabled = db.Column(db.Boolean, nullable=True, default=False)

    products = db.Column(db.String(550), nullable=True)
    last_login = db.Column(BigInteger, nullable=True, default=func.extract('epoch', func.current_timestamp()))
    is_active = db.Column(db.Boolean, default=False)

    is_lender = db.Column(db.Boolean, default=False)
    is_borrower = db.Column(db.Boolean, default=False)
    question_1 = db.Column(db.String(350), nullable=True)
    question_2 = db.Column(db.String(350), nullable=True)
    question_3 = db.Column(db.String(350), nullable=True)
    answer_1 = db.Column(db.String(350), nullable=True)
    answer_2 = db.Column(db.String(350), nullable=True)
    answer_3 = db.Column(db.String(350), nullable=True)
    status = db.Column(db.String(350), nullable=True)

    credit_reports_sent = db.Column(db.Integer(), default=0)
    status_updated_on = db.Column(BigInteger, nullable=True)
    is_staff = db.Column(db.Boolean, default=False)
    referral_code = db.Column(db.String(350), nullable=True)
    is_superuser = db.Column(db.Boolean, default=False)
    receive_notifications = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(350), default='3kle-app-user')
    is_basic_info_completed = db.Column(db.Boolean, default=False)
    has_loan = db.Column(JSON, default={'type': '', 'status': False})

    individual_account_number = db.Column(db.Integer(), nullable=True)
    saved_beneficiaries = db.Column(JSON, nullable=True)
    is_phone_verified = db.Column(db.Boolean, default=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    email_verified_on = db.Column(BigInteger, nullable=True)
    phone_verified_on = db.Column(BigInteger, nullable=True)
    phone_verification_failed_attempts = db.Column(db.Integer(), default=0)
    email_verification_failed_attempts = db.Column(db.Integer(), default=0)
    user_subscription_plan = db.Column(db.String(350), default='STARTER')

    referrals = db.relationship("Referral", back_populates='user')
    business = db.relationship("Business", backref='user')
    accounts = db.relationship("Account", cascade="all,delete", back_populates='user')
    notifications = db.relationship("Notification", cascade="all,delete", back_populates='user')
    update_profile_request = db.relationship("UpdateProfileRequest", cascade="all,delete", back_populates='user')
    phone_verifications = db.relationship("PhoneVerification", cascade="all,delete", back_populates='user')
    bill_payments = db.relationship("BillPayment", cascade="all,delete", back_populates='user')
    budget_spending = db.relationship("BudgetSpending", cascade="all,delete", back_populates='user')
    verifications = db.relationship("Verification", cascade="all,delete", back_populates='user')
    credit_score = db.relationship("CreditScore", cascade="all,delete", back_populates='user')
    transactions = db.relationship("Transaction", foreign_keys="Transaction.user_id", back_populates='user')
    sent_transactions = db.relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = db.relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")
    emergency_savings = db.relationship("EmergencySavings", cascade="all,delete", back_populates='user')
    goal_savings = db.relationship("GoalSavings", cascade="all,delete", back_populates='user')
    overdraft = db.relationship("Overdraft", cascade="all,delete", back_populates='user')

    notification_settings = db.Column(JSON, default={
        "Transaction": {
            "SMS": False,
            "Email": True,
            "Push": False
        },
        "New_Card_Issue": {
            "SMS": False,
            "Email": True,
            "Push": False
        },
        "Amend_Regular_Payment": {
            "SMS": False,
            "Email": True,
            "Push": False
        },
        "Update_Contact_Details": {
            "SMS": False,
            "Email": True,
            "Push": False
        },
        "Unrecognized_Location": {
            "SMS": False,
            "Email": True,
            "Push": True
        }
    })

    @validates('saved_beneficiaries')
    def validate_saved_beneficiaries(self, value):
        valid_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "Column"},
                    "full_name": {"type": "Column"},
                    "account_number": {"type": "Column", "pattern": "^\\d{10}$"},
                    "bank_code": {"type": "Column"},
                    "is_3kle": {"type": "Column"},
                    "bank_name": {"type": "Column"}
                },
                "required": ["account_number", "bank_code", "is_3kle", "bank_name", "full_name"],
                "additionalProperties": False
            }
        }

        try:
            jsonschema.validate(value, valid_schema)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)

    # ===================  STATIC METHODS  =======================

    def update_user(self, updates: dict) -> dict:
        valid_attributes = [column.key for column in self.__table__.columns]

        valid_updates = {key: value for key, value in updates.items() if key in valid_attributes}

        for key, value in valid_updates.items():
            setattr(self, key, value)

        db.session.commit()
        return valid_updates

    def get_user_by_id(self, user_id: str) -> dict:
        user = self.query.filter_by(id=user_id).first()
        if not user:
            return {}

        return user.to_dict()

    def get_user_by_phone_number(self, phone_number: str) -> dict:
        user = self.query.filter_by(phone_number=phone_number).first()
        if not user:
            return {}

        return user.to_dict()

    def get_user_by_email(self, email: str) -> dict:
        user = self.query.filter_by(email=email).first()
        if not user:
            return {}

        return user.to_dict()

    def set_loan_status(self, new_status: bool, loan_type: str = "") -> dict:
        """
        Updates the user's loan status

        Parameters:
        1. new_status (bool): The new status to update to. True if user has a loan that's not completed, otherwise false
        3. loan_type (str): The loan type. This is only applicable when the loan status is being set to True
        """
        if not new_status: loan_type = ""

        loan_status = self.has_loan['status']

        if loan_status and loan_status == new_status: raise CustomException(ExceptionCode.LOAN_EXIST)  # noqa : E701

        self.has_loan = {'status': new_status, 'type': loan_type}
        db.session.commit()

        return self.has_loan

    @staticmethod
    def hash_key(value):
        hash_value = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        return hash_value.decode()

    def isCorrectPin(self, user_pin: str) -> bool:
        """

        Parameters:
        2. user_pin (str): this the pin passed by the user
        """

        if bcrypt.checkpw(str(user_pin).encode(), self.pin.encode()):
            return True
        else:
            raise CustomException(ExceptionCode.INVALID_TRANSACTION_PIN)

    @staticmethod
    def add_user_to_cognito(user_id, email, phone_number, password, user_type):
        try:
            cognito_client = boto3.client('cognito-idp')
            client_id = CLIENT_ID
            user_pool_id = USER_POOL_ID

            user_id = str(user_id)
            # Register/adding user to cognito with unconfirm status
            response = cognito_client.sign_up(
                Username=user_id,
                Password=password,
                ClientId=client_id,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'profile', 'Value': email},
                    {'Name': 'phone_number', 'Value': phone_number},
                    {'Name': 'custom:user_type', 'Value': user_type},
                    {'Name': 'custom:uuid', 'Value': user_id}
                ]
            )

            return True

        except cognito_client.exceptions.UsernameExistsException as e:
            raise CustomException(ExceptionCode.USER_EXISTS)

        except Exception as e:
            print_exc()
            raise e
