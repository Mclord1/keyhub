from . import *
from ..Schema.school import UpdateSchoolSchema, SchoolSchema


class SchoolModel:

    @classmethod
    def toggle_status(cls, school_id):
        _school: School = School.GetSchool(school_id)

        _school.isDeactivated = not _school.isDeactivated
        db.session.commit()
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

        return {
            "num_of_teachers": len(_school.teachers),
            "num_of_students": len(_school.students),
            "num_of_parents": len(_school.parents),
            "num_of_school_administrators": len(_school.managers),
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
        return f"School information has been updated successfully"

    @classmethod
    def add_school(cls, data):
        req_schema: SchoolSchema = validator.validate_data(SchoolSchema, data)

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

        try:

            # Add school details to school model
            add_school = School(name=name, email=email, msisdn=msisdn, reg_number=reg_number, country=country,
                                state=state, address=address)
            add_school.save(refresh=True)

            Helper.User_Email_OR_Msisdn_Exist(primary_contact.email, primary_contact.msisdn)

            role = Role.GetRoleByName(BasicRoles.SCHOOL_ADMIN.value)

            # create the user account on User model
            user = User.CreateUser(primary_contact.email, primary_contact.msisdn, role)

            # create and add school admin
            add_school_admin = SchoolManager(
                school_id=add_school.id,
                name=primary_contact.name,
                gender=primary_contact.gender,
                residence=primary_contact.address,
                user_id=user.id
            )

            add_school_admin.save(refresh=True)

            return f"The school {add_school.name} has been added successfully"
        except Exception as e:
            db.session.rollback()
            print(e)
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
                    "role": x.user.roles.name if x.user.roles else None,
                    "email": x.user.email,
                    "isDeactivated": x.user.isDeactivated,
                    "msisdn": x.user.msisdn,
                    **x.to_dict(add_filter=False)
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
                    **teacher.to_dict()
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
                    **parent.to_dict()
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
                    **student.to_dict()
                } for student in results]
            }

        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_transactions(cls, school_id):
        pass

    @classmethod
    def get_subscriptions(cls, school_id):
        pass

    @classmethod
    def get_profile_settings(cls, school_id):
        pass
