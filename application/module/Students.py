from . import *


class StudentModel:

    @classmethod
    def get_all_students(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _students = Student.query.order_by(desc(Student.created_at)).paginate(page=page, per_page=per_page,
                                                                              error_out=False)
        total_items = _students.total
        results = [item for item in _students.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_students": len([x for x in results if x.user.isDeactivated]),
                "num_of_active_students": len([x for x in results if not x.user.isDeactivated]),
                "num_of_students": len(results),
                "students": [{
                    **(res.user.as_dict() if res.user else {}),
                    **res.to_dict(),
                    "user_id": res.user.id,
                    "project": [x.to_dict(add_filter=False) for x in res.projects],
                    "parent": [{**x.to_dict(), **x.user.as_dict(), 'user_id': x.user.id} for x in res.parents],
                    "school": res.schools.name,
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        user: User = User.GetUser(user_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        if not data:
            raise CustomException(message="Please provide data to update", status_code=400)

        gender = data.get('gender')
        role = data.get('role')
        if role:
            user.role_id = role
        if gender:
            user.students.gender = gender
        user.students.update_table(data)
        Audit.add_audit('Updated Student Information', current_user, user.to_dict())
        return {**user.students.to_dict(), "user_id": user.id}

    @classmethod
    def add_student(cls, data):
        req: StudentSchema = validator.validate_data(StudentSchema, data)

        if req.email and req.msisdn:
            Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRoleByName(BasicRoles.STUDENT.value)

        school: School = School.GetSchool(req.school_id)

        if req.profile_image:

            file_path = FileFolder.student_profile(school.name, req.email)

            profile_url = FileHandler.upload_file(req.profile_image, file_path)
        else:
            profile_url = None

        _parent = []
        if req.parent:
            u_parent: User = User.GetUser(req.parent)

            if not u_parent.parents:
                raise CustomException(message="Parent not found", status_code=404)

            _parent = [u_parent.parents]

        new_student = User(email=req.email, msisdn=req.msisdn, password=None)
        new_student.roles = role
        db.session.add(new_student)
        db.session.commit()
        db.session.refresh(new_student)

        try:

            if new_student:
                student_data = {
                    field: getattr(req, field)
                    for field in req.model_fields.keys()
                }
                # Remove None values for optional fields
                student_data = {k: v for k, v in student_data.items() if v is not None}

                # Add additional data not included in StudentSchema
                student_data.update({
                    'user_id': new_student.id,
                    'profile_image': profile_url,
                    'parents': _parent,
                    'schools': school,
                })

                # remove this as it is already added in user table
                del student_data['email']
                del student_data['msisdn']
                del student_data['learning_group_id']

                add_user = Student(**student_data)

                if req.learning_group_id:
                    _learning_group: LearningGroup = LearningGroup.GetLearningGroupID(req.school_id, req.learning_group_id)

                    _learning_group.students.append(add_user)

                add_user.save(refresh=True)
                EmailHandler.welcome_mail(new_student.email, add_user.first_name)

                return {**add_user.to_dict(), "user_id": add_user.user.id}

        except Exception as e:
            db.session.rollback()
            # Delete the new_student instance
            if new_student:
                db.session.delete(new_student)
            raise e

    @classmethod
    def remove_parent(cls, student_id, parent_id):

        u_student: User = User.GetUser(student_id)
        u_parent: User = User.GetUser(parent_id)

        if not u_student.students:
            raise CustomException(message="Student does not exist", status_code=404)

        if not u_parent.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        if u_student.students not in [x for x in u_parent.parents.students]:
            raise CustomException(message="Student Not Found")

        u_student.students.parents.remove(u_parent.parents)
        db.session.commit()
        return "Parent has been successfully removed"

    @classmethod
    def add_parent(cls, student_id, parent_id):
        u_student: User = User.GetUser(student_id)
        u_parent: User = User.GetUser(parent_id)

        if not u_student.students:
            raise CustomException(message="Student does not exist", status_code=404)

        if not u_parent.parents:
            raise CustomException(message="Parent does not exist", status_code=404)

        if u_student.students.schools not in [x for x in u_parent.parents.schools]:
            raise CustomException(message="Student must belong to same school as parent")

        u_student.students.parents.append(u_parent.parents)
        db.session.commit()
        return "Parent has been successfully added"

    @classmethod
    def change_student_profile_image(cls, profile_image, student_id):
        if not profile_image:
            raise CustomException(message="User profile image is required")

        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        file_path = FileFolder.student_profile(user.students.schools.name, user.email)

        profile_url = FileHandler.upload_file(profile_image, file_path)

        user.students.profile_image = profile_url
        db.session.commit()
        return "Profile Image has been updated successfully"

    @classmethod
    def reset_password(cls, user_id):
        user: User = User.GetUser(user_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        Audit.add_audit('Reset Student password', current_user, user.to_dict())
        return Helper.send_otp(user)

    @classmethod
    def deactivate_user(cls, user_id, reason):
        user: User = User.GetUser(user_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        Audit.add_audit('Changed Student Account Status', current_user, user.to_dict())

        return Helper.disable_account(user, reason)

    @classmethod
    def search_students(cls, args):
        return Helper.look_up_account(Student, User, args)

    @classmethod
    def get_user(cls, user_id):

        user: User = User.GetUser(user_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        _user: Student = Helper.get_user(Student, user.students.id)

        file_path = FileFolder.student_profile(_user.schools.name, user.email)

        return {
            **_user.to_dict(),
            **_user.user.as_dict(),
            "user_id": user.id,
            "profile_image": FileHandler.get_file_url(str(file_path)),
            "learning_groups": [{'name': x.name, 'id': x.id} for x in _user.learning_groups],
            "parent": [{**x.to_dict(), 'user_id': x.user.id} for x in _user.parents],
            "projects": [{'name': x.name, 'id': x.id} for x in _user.projects]
        }

    @classmethod
    def add_comment(cls, student_id, comment):

        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        new_comment = StudentComment(student_id=user.students.id, user_id=current_user.id, comment=comment)
        new_comment.save(refresh=True)
        return "Comment has been added successfully"

    @classmethod
    def get_comments(cls, student_id):
        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)
        return [
            {
                **x.to_dict(add_filter=False),
                "commented_by": {
                    **user.GetUserObject(x.user.id)
                },

            }
            for x in user.students.student_comments]

    @classmethod
    def edit_comments(cls, student_id, comment_id, new_comment):

        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        comments: StudentComment = StudentComment.query.filter_by(student_id=user.students.id, id=comment_id).first()

        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers or current_user.id != comments.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        comments.comment = new_comment
        db.session.commit()
        return "Comment has been updated successfully"

    @classmethod
    def remove_comment(cls, student_id, comment_id):

        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        comments: StudentComment = StudentComment.query.filter_by(student_id=user.students.id, id=comment_id).first()
        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers or current_user.id != comments.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        comments.delete()
        return "Comment has been deleted successfully"

    @classmethod
    def add_file(cls, student_id, file, file_name):
        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        file_path, stored_file_name = FileFolder.student_file(user.students.schools.name, user.email, file_name)

        profile_url = FileHandler.upload_file(file, file_path)

        new_file = StudentFile(student_id=user.students.id, file_name=stored_file_name, file_url=profile_url,
                               file_path=file_path,
                               user_id=current_user.id)
        new_file.save()
        return "File has been added successfully"

    @classmethod
    def get_files(cls, student_id):
        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        return [
            {
                **x.to_dict(add_filter=False),
                "uploaded_by": x.user.to_dict() | User.GetUserObject(x.user.id),
                "file_url": FileHandler.get_file_url(x.file_path)

            }
            for x in user.students.student_files]

    @classmethod
    def remove_file(cls, student_id, file_id):

        user: User = User.GetUser(student_id)

        if not user.students:
            raise CustomException(message="Student does not exist", status_code=404)

        _files: StudentFile = StudentFile.query.filter_by(student_id=user.students.id, id=file_id).first()

        if not _files:
            raise CustomException(message="File not found", status_code=404)

        if not current_user.managers or current_user.id != _files.user_id:
            if not current_user.admins:
                raise CustomException(message="Only File author or admin can delete this File", status_code=400)

        FileHandler.delete_file(_files.file_path)
        _files.delete()
        return "File has been deleted successfully"
