from . import *


class ParentModel:

    @classmethod
    def get_all_parents(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _parents = Parent.query.order_by(desc(Parent.created_at)).paginate(page=page, per_page=per_page,
                                                                           error_out=False)
        total_items = _parents.total
        results = [item for item in _parents.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_parents": len([x for x in results if x.user.isDeactivated]),
                "num_of_active_parents": len([x for x in results if not x.user.isDeactivated]),
                "num_of_parents": len(results),
                "parents": [{
                    **(res.user.as_dict() if res.user else {}),
                    **res.to_dict(),
                    "user_id": res.user.id,
                    "schools": [{"name": x.name} for x in res.schools],
                    "num_of_children": len(res.students) if res and res.students else 0,
                    "num_of_active_children": len([x for x in res.students if not x.user.isDeactivated]),
                    "num_of_deactivated_children": len([x for x in res.students if x.user.isDeactivated]),
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):

        user: User = User.GetUser(user_id)

        if not user.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        if not data:
            raise CustomException(message="Please provide data to update", status_code=400)

        gender = data.get('gender')
        role = data.get('role')
        if role:
            user.role_id = role
        if gender:
            user.parents.gender = gender
        user.parents.update_table(data)
        Audit.add_audit('Updated Parent Information ', current_user, user.parents.to_dict())
        return {**user.parents.to_dict(), "user_id": user.id}

    @classmethod
    def add_parent(cls, data):
        req: ParentSchema = validator.validate_data(ParentSchema, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.PARENT.value)

        _school = School.GetSchool(req.school_id)


        try:

            students_list = [User.GetUser(x).students for x in req.student] if req.student else []

            if req.student and None in students_list:
                raise CustomException(message="Please ensure the student passed already exist")

            else:

                new_parent = User.CreateUser(req.email, req.msisdn, role)

                add_parent = Parent(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_parent.id,
                    address=req.address,
                    gender=req.gender,
                    work_email=req.work_email,
                    work_address=req.work_address,
                    relationship_to_student=req.relationship_to_student,
                    work_msisdn=req.work_msisdn,
                    how_you_knew_about_us=req.how_you_knew_about_us,
                    why_use_us=req.why_use_us,
                    current_school=req.current_school,
                    date_to_join=req.date_to_join,
                    languages_spoken_at_home=req.languages_spoken_at_home,
                    child_first_language=req.child_first_language,
                    has_emailed_child_kyc=req.has_emailed_child_kyc,
                    agree_with_terms=req.agree_with_terms
                )

                add_parent.schools.append(_school)
                add_parent.save(refresh=True)
                EmailHandler.welcome_mail(new_parent.email, add_parent.first_name)
                return {**add_parent.to_dict(), "user_id": add_parent.user.id}

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def add_student(cls, student_id, parent_id):

        u_student: User = User.GetUser(student_id)
        u_parent: User = User.GetUser(parent_id)

        if not u_student.students:
            raise CustomException(message="Student does not exist", status_code=404)

        if not u_parent.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        if u_student.students.schools not in [x for x in u_parent.parents.schools]:
            raise CustomException(message="Student must belong to same school as parent")

        u_parent.parents.students.add(u_student.students)
        db.session.commit()
        return "Student has been added successfully"

    @classmethod
    def remove_student(cls, student_id, parent_id):

        u_student: User = User.GetUser(student_id)
        u_parent: User = User.GetUser(parent_id)

        if not u_student.students:
            raise CustomException(message="Student does not exist", status_code=404)

        if not u_parent.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        if u_student.students not in [x for x in u_parent.parents.students]:
            raise CustomException(message="Student Not Found")

        u_parent.parents.students.remove(u_student.students)
        db.session.commit()
        return "Student has been removed successfully"

    @classmethod
    def reset_password(cls, user_id):

        user: User = User.GetUser(user_id)

        if not user.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        Audit.add_audit('Reset Parent Password ', current_user, user.to_dict())
        return Helper.send_otp(user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        user: User = User.GetUser(user_id)

        if not user.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        Audit.add_audit('Changed Parent account status ', current_user, user.to_dict())
        return Helper.disable_account(user, reason)

    @classmethod
    def search_parents(cls, args):
        return Helper.look_up_account(Parent, User, args)

    @classmethod
    def get_user(cls, user_id):

        user: User = User.GetUser(user_id)

        print(user)

        if not user.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        _user = Helper.get_user(Parent, user.parents.id)

        return {
            **_user.to_dict(),
            **_user.user.as_dict(),
            "user_id": user.id,
            "students": [
                {
                    **x.to_dict(),
                    "school": x.schools.name,
                    "user_id": x.user.id,
                    "file_url": [FileHandler.get_file_url(x.file_path) for x in x.student_files]
                }
                for x in _user.students],
            "schools": [x.to_dict(add_filter=False) for x in _user.schools]
        }
