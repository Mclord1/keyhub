import sys
from os.path import dirname, abspath

from application.Enums.Permission import PermissionEnum

sys.path.append(dirname(abspath(__file__)))

from sqlalchemy.exc import IntegrityError

from application import db, app
from application.models import *


class Seed:

    @staticmethod
    def AddRole():
        add_roles = ['system_admin', 'school_admin', 'teacher', 'student', 'parent']

        for role in add_roles:
            try:
                new_role = Role(name=role)
                new_role.save(refresh=True)
            except IntegrityError:
                db.session.rollback()
        print("Role Model has been added")

    @staticmethod
    def AddPermission():

        add_permissions = [x.value for x in PermissionEnum.__members__.values()]

        admin_role = Role.query.filter_by(id=1).first()
        for permissions in add_permissions:
            try:
                new_permission = Permission(name=permissions)
                new_permission.roles.append(admin_role)
                new_permission.save(refresh=True)

            except IntegrityError:
                db.session.rollback()
        print("Permission has been added successfully")

    @staticmethod
    def AddAdmin():
        create_admin = {
            "email": "clairclancy@gmail.com",
            "msisdn": "+2348037144591",
            "first_name": "john",
            "last_name": "doe",
            "gender": "Male",
            "country": "Nigeria",
            "state": "Lagos",
            "address": "15b ikeja road",
            "role": 1,
            "img": "1.jpg"
        }

        user: User = User.query.filter_by(email=create_admin['email']).first()

        if not user:
            role = Role.GetRole(create_admin['role'])
            try:
                new_admin = User.CreateUser(create_admin['email'], create_admin['msisdn'], role)
                if new_admin:
                    add_user = Admin(
                        first_name=create_admin['first_name'],
                        last_name=create_admin['last_name'],
                        country=create_admin['country'],
                        state=create_admin['state'],
                        user_id=new_admin.id,
                        residence=create_admin['address'],
                        gender=create_admin['gender'],
                    )
                    add_user.save(refresh=True)

            except IntegrityError:
                db.session.rollback()

            print("Admin has been created successfully")

    def RunSeed(self):
        """
             Implementation scripts to automate the creation of the database and seeding with initial data.
             This ensures that all developers have the same initial data for testing and development.
        """
        self.AddRole()
        self.AddPermission()
        self.AddAdmin()


with app.app_context():
    # Create and add records to the database
    Seed().RunSeed()
