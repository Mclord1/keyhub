from collections import defaultdict

from . import *
from ..Schema.school import UpdateSchoolSchema, SchoolSchema


class SchoolModel:

    @classmethod
    def toggle_status(cls, school_id):
        _school: School = School.GetSchool(school_id)

        _school.isDeactivated = not _school.isDeactivated
        db.session.commit()
        Audit.add_audit("Deactivated School" if _school.isDeactivated else "Activate School", current_user, _school.to_dict(add_filter=False))

        return "School has been deactivated" if _school.isDeactivated else "School has been activated"

    @classmethod
    def list_all_schools(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _school: School = School.query.order_by(desc(School.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _school.total
        results = [item for item in _school.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "total_schools": len(results),

                "total_active_schools": len([x for x in results if not x.isDeactivated]),
                "total_deactivated_schools": len([x for x in results if x.isDeactivated]),
                "schools": [{
                    **school.to_dict(add_filter=False),
                    "total_learning_groups": len(school.learning_groups),
                    "learning_groups": [x.id for x in school.learning_groups],
                    "num_of_teachers": len(school.teachers) if school.teachers else 0,
                    "num_of_students": len(school.students) if school.students else 0,
                    "num_of_parents": len(school.parents) if school.parents else 0,
                    "num_of_school_administrators": len(school.managers) if school.managers else 0,
                } for school in results],

            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def view_school_info(cls, school_id):
        _school: School = School.GetSchool(school_id)
        sub: Subscription = Subscription.query.filter(Subscription.school_id == _school.id, Subscription.status == "active").first()
        subcription_plan = sub.subscription_plan.name if sub else None

        # Collecting students per month for each project
        students_per_month = defaultdict(int)

        for project in _school.projects:
            for student in project.students:
                # Assuming the 'enrollment_date' field exists in the Student model
                month_year = datetime.datetime.fromtimestamp(student.created_at).strftime("%Y-%m")  # Format: YYYY-MM
                students_per_month[month_year] += 1

        return {
            "num_of_teachers": len(_school.teachers),
            "num_of_students": len(_school.students),
            "num_of_parents": len(_school.parents),
            "num_of_school_administrators": len(_school.managers),
            "learning_groups": [x.id for x in _school.learning_groups],
            "subcription_plan": subcription_plan,
            "next_subscription_plan": sub.next_billing_date if sub else None,
            "faqs": [x.to_dict(add_filter=False) for x in _school.faqs],
            "student_by_gender": {
                "male": {
                    "count": len([x for x in _school.students if x.gender == "Male"]),
                    "percentage": (len([x for x in _school.students if x.gender == "Male"]) * 100) / len(
                        _school.students) if _school.students else 0
                },
                "female": {
                    "count": len([x for x in _school.students if x.gender == "Female"]),
                    "percentage": (len([x for x in _school.students if x.gender == "Female"]) * 100) / len(
                        _school.students) if _school.students else 0
                }
            },
            "teachers_by_gender": {
                "male": {
                    "count": len([x for x in _school.teachers if x.gender == "Male"]),
                    "percentage": (len([x for x in _school.teachers if x.gender == "Male"]) * 100) / len(
                        _school.teachers) if _school.teachers else 0
                },
                "female": {
                    "count": len([x for x in _school.teachers if x.gender == "Female"]),
                    "percentage": (len([x for x in _school.teachers if x.gender == "Female"]) * 100) / len(
                        _school.teachers) if _school.teachers else 0
                }
            },
            "students_per_month": students_per_month,
            **_school.to_dict(add_filter=False)
        }

    @classmethod
    def update_school(cls, school_id, data):
        req_school = validator.validate_data(UpdateSchoolSchema, data)

        school: School = School.query.filter_by(id=school_id).first()

        if not school:
            raise CustomException(message="School not found", status_code=403)

        _school: School = School.query.filter(
            (School.name == req_school.name) |
            (School.email == req_school.email) |
            (School.msisdn == req_school.msisdn) |
            (School.reg_number == req_school.reg_number)
        ).first()

        if _school and _school.id != school_id:
            existing_values = []

            if _school.name == req_school.name:
                existing_values.append("name")
            if _school.email == req_school.email:
                existing_values.append("email")
            if _school.msisdn == req_school.msisdn:
                existing_values.append("msisdn")
            if _school.reg_number == req_school.reg_number:
                existing_values.append("reg_number")

            raise CustomException(message=f"School attributes already exist: {', '.join(existing_values)}",
                                  status_code=403)

        school.update_table(data)
        Audit.add_audit('Updated School Information', current_user, school.to_dict(add_filter=False))

        return f"School information has been updated successfully"

    @classmethod
    def add_school(cls, data):
        req_schema: SchoolSchema = validator.validate_data(SchoolSchema, data)

        profile_url = FileHandler.upload_file(req_schema.profile_image, FileFolder.school(req_schema.name))

        name = req_schema.name
        email = req_schema.email
        msisdn = req_schema.msisdn
        reg_number = req_schema.reg_number
        country = req_schema.country
        state = req_schema.state
        address = req_schema.address
        primary_contact = req_schema.primary_contact

        _school: School = School.query.filter(
            (School.name == name) |
            (School.email == email) |
            (School.msisdn == msisdn) |
            (School.reg_number == reg_number)
        ).first()

        if _school:
            existing_values = []

            if _school.name == req_schema.name:
                existing_values.append("name")
            if _school.email == req_schema.email:
                existing_values.append("email")
            if _school.msisdn == req_schema.msisdn:
                existing_values.append("msisdn")
            if _school.reg_number == req_schema.reg_number:
                existing_values.append("reg_number")

            raise CustomException(message=f"School attributes already exist: {', '.join(existing_values)}",
                                  status_code=403)

        Helper.User_Email_OR_Msisdn_Exist(primary_contact.email, primary_contact.msisdn)

        try:

            # Add school details to school model
            add_school = School(name=name, email=email, msisdn=msisdn, reg_number=reg_number, country=country,
                                state=state, address=address, logo=str(profile_url))
            add_school.save(refresh=True)

            # create school role for school_admin
            _role = SchoolRole(name=BasicRoles.SCHOOL_ADMIN.value, admin_id=current_user.id, description='School admin role', schools=add_school)
            _role.save(refresh=True)

            # create the user account on User model
            new_admin = User(email=primary_contact.email, msisdn=primary_contact.msisdn, password=None)
            permissions_all = SchoolPermission.query.all()
            db.session.add(new_admin)
            new_admin.save(refresh=True)

            # create and add school admin
            add_school_admin = SchoolManager(
                school_id=add_school.id,
                name=primary_contact.name,
                gender=primary_contact.gender,
                residence=primary_contact.address,
                user_id=new_admin.id
            )
            add_school_admin.school_roles = _role
            add_school_admin.save(refresh=True)
            EmailHandler.welcome_mail(new_admin.email, add_school_admin.name)

            # assign school permissions to the school admin role
            add_school_admin.school_roles.school_permissions.extend(permissions_all)
            db.session.commit()

            # TODO :: Add background service to image processing

            # save image to table
            add_school.update_table({'logo': profile_url})

            Audit.add_audit('Added School', current_user, add_school.to_dict(add_filter=False))

            return f"The school {add_school.name} and admin has been added successfully"
        except IntegrityError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_account_admins(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _school_admin: SchoolManager = SchoolManager.query.filter(SchoolManager.school_id == school_id).order_by(
            desc(SchoolManager.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _school_admin.total
        results = [item for item in _school_admin.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_admins": len(results),
                "num_of_active_admins": len([x for x in results if not x.user.isDeactivated]),
                "num_of_deactivated_admins": len([x for x in results if x.user.isDeactivated]),
                "admins": [{
                    "role": x.school_roles.name if x.school_roles else None,
                    "email": x.user.email,
                    "isDeactivated": x.user.isDeactivated,
                    "msisdn": x.user.msisdn,
                    **x.to_dict(add_filter=False),
                    "user_id": x.user.id
                } for x in results]
            }
        }

        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_teachers(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _teacher: Teacher = Teacher.query.join(School.teachers).filter(School.id == school_id).order_by(
            desc(Teacher.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _teacher.total
        results = [item for item in _teacher.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_teachers": len(results),
                "num_of_active_teachers": len([x for x in results if not x.user.isDeactivated]),
                "num_of_deactivated_teachers": len([x for x in results if x.user.isDeactivated]),
                "teachers": [{
                    "email": teacher.user.email,
                    "isDeactivated": teacher.user.isDeactivated,
                    "msisdn": teacher.user.msisdn,
                    "num_of_projects": len([x for x in teacher.projects]),
                    "num_of_students": len([x for x in teacher.students]),
                    **teacher.to_dict(),
                    "user_id": teacher.user.id
                } for teacher in results]
            }
        }

        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_parents(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _parent: Parent = Parent.query.join(School.parents).filter(School.id == school_id).order_by(
            desc(Parent.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _parent.total
        results = [item for item in _parent.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_parents": len(results),
                "num_of_active_parents": len([x for x in results if not x.user.isDeactivated]),
                "num_of_deactivated_parents": len([x for x in results if x.user.isDeactivated]),
                "parents": [{
                    "email": parent.user.email,
                    "isDeactivated": parent.user.isDeactivated,
                    "msisdn": parent.user.msisdn,
                    "num_of_children": len([x for x in parent.students if x.school_id == school_id]),
                    "num_of_active_children": len([student for student in parent.students if
                                                   student.school_id == school_id and not student.user.isDeactivated]),
                    "num_of_deactivated_children": len([student for student in parent.students if
                                                        student.school_id == school_id and student.user.isDeactivated]),
                    **parent.to_dict(),
                    "user_id": parent.user.id
                } for parent in results]
            }
        }

        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_students(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _student: Student = Student.query.filter(Student.school_id == school_id).order_by(
            desc(Student.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _student.total
        results = [item for item in _student.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_students": len(results),
                "num_of_active_students": len([x for x in results if not x.user.isDeactivated]),
                "num_of_deactivated_students": len([x for x in results if x.user.isDeactivated]),
                "students": [{
                    "project": [x.to_dict(add_filter=False) for x in student.projects],
                    "email": student.user.email,
                    "isDeactivated": student.user.isDeactivated,
                    "msisdn": student.user.msisdn,
                    **student.to_dict(),
                    "user_id": student.user.id
                } for student in results]
            }

        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_profile_settings(cls, school_id):
        pass

    @classmethod
    def search_schools(cls, args):
        query = School.query.filter(
            (School.name.ilike(f'%{args}%'))
        )
        result = [
            {
                **x.to_dict(add_filter=False),
            }

            for x in query.all()
        ]
        return result
