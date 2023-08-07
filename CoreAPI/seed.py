import sys
from os.path import dirname, abspath
import time

from sqlalchemy.exc import IntegrityError

sys.path.append(dirname(dirname(abspath(__file__))))

from submodule_models_3kle import db, app
from app.models import User
from submodule_models_3kle.models import ChannelEnum, Channel, Account, AccountTypeEnum, Transaction, BudgetCategory
from submodule_util_3kle.util.cognito.user_registration import add_user_to_cognito_user_pool_and_app_user, \
    initiate_auth_process, confirm_user_to_cognito_user_pool_by_admin, generate_account_number, generate_hash
from submodule_util_3kle.util.get_cognito_client import cognito_client
from submodule_util_3kle.util.get_cognito_client import USER_POOL_ID


class Seed:
    @staticmethod
    def AddUser(email, phone_number, password, fname, lname, dob, gender):
        user_type = "3kle-app-user"

        try:
            user_data = User(
                email=email,
                phone_number=phone_number,
                status='USER_REGISTERED_ON_COGNITO',
                status_updated_on=int(time.time())
            )

            db.session.add(user_data)
            db.session.commit()
            db.session.refresh(user_data)

            # Register/adding user to cognito user pool and to database
            add_user_to_cognito_user_pool_and_app_user(user_data.id, email, phone_number, password, user_type)

            # Confirming user status by admin on cognito user pool
            confirm_user_to_cognito_user_pool_by_admin(str(user_data.id))

            # Initiate auth process so access token can be generated
            access_token = initiate_auth_process(str(user_data.id), password)

            # Automatically verify email and phone number
            response = cognito_client.admin_update_user_attributes(
                UserPoolId=USER_POOL_ID,
                Username=str(user_data.id),
                UserAttributes=[
                    {'Name': 'phone_number_verified', 'Value': 'true'},
                    {'Name': 'email_verified', 'Value': 'true'},
                ],
            )

            cognito_client.admin_enable_user(UserPoolId=USER_POOL_ID, Username=str(user_data.id))

            user_data.is_staff = False
            user_data.is_active = True
            user_data.user_type = '3kle-app-user'
            user_data.status = 'BASIC_INFO_COMPLETED'
            user_data.is_basic_info_completed = True

            account_number = generate_account_number(AccountTypeEnum.PERSONAL.value)

            add_account = Account(user_id=user_data.id, account_number=account_number, account_type=AccountTypeEnum.PERSONAL.value)  # noqa
            db.session.add(add_account)
            db.session.commit()

            user_data.gender = gender
            user_data.last_name = lname
            user_data.first_name = fname
            user_data.date_of_birth = dob
            user_data.country = "Nigeria"
            user_data.country_code = "+234"
            user_data.is_active = True
            user_data.pin = "1234"

            user_data.pin = generate_hash(user_data.pin)

            db.session.add(user_data)
            db.session.commit()

            print(f"\n========================= User created successfully ==========================")
            login_details = {'phone_number': phone_number, 'password': password}
            print(f"Login details : {login_details}")

        except IntegrityError:
            db.session.rollback()

            print(f"\n=========================== User already exists ==============================")
            login_details = {'phone_number': phone_number, 'password': password}
            print(f"Login details : {login_details}")

    @staticmethod
    def AddUsers():
        users = [
            {
                'email': 'testuser1@3kle.com',
                'phone_number': '+2348167151000',
                'password': 'Test@12345',
                'fname': 'test1',
                'lname': 'user1',
                'dob': '18/05/2000',
                'gender': 'Male'
            },
            {
                'email': 'testuser2@3kle.com',
                'phone_number': '+2348167151001',
                'password': 'Test@12345',
                'fname': 'test2',
                'lname': 'user2',
                'dob': '18/05/2000',
                'gender': 'Male'
            }
        ]

        for user in users:
            Seed.AddUser(
                user['email'], user['phone_number'],
                user['password'], user['fname'],
                user['lname'], user['dob'], user['gender']
            )

    @staticmethod
    def AddChannel():
        _ = [channel.value for channel in ChannelEnum]
        try:
            for channel in _:
                add_channel = Channel(name=channel, active=True)  # noqa
                db.session.add(add_channel)
                db.session.commit()
                print(f"Channel records has been added")

        except IntegrityError:
            db.session.rollback()
            print(f"Channel records has been added")

    @staticmethod
    def FundAccount():
        personal_account : Account = Account.get_personal_account(14)
        Transaction.transfer_b2a(amount=100000, channel_name=ChannelEnum.TRIKLE_B2C, receiver_account=personal_account)
        print("========= Account has been credited with 100,000 =========")

    @staticmethod
    def AddBudgetCategories():
        _ = ['Internet', 'Health', 'Food', 'Others', 'Gifts', 'Education', 'Entertainment', 'Betting', 'Housing', 'Transport', 'Groceries', 'Shopping']
        try:
            for x in _:
                budget = BudgetCategory(name=x)  # noqa
                db.session.add(budget)
                db.session.commit()
            print("========== Budget category created successfully ===========")
        except IntegrityError:
            print("========== Budget category has already been created ===========")
            db.session.rollback()

    def RunSeed(self):
        """
             Implementation scripts to automate the creation of the database and seeding with initial data.
             This ensures that all developers have the same initial data for testing and development.
        """

        self.AddChannel()
        self.AddUsers()
        self.AddBudgetCategories()
        self.FundAccount()


with app.app_context():
    # Create and add records to the database
    Seed().RunSeed()
