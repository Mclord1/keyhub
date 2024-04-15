from . import *


class SystemAdmins:

    @classmethod
    def create_admin(cls, data):

        req: SystemAdminSchema = validator.validate_data(SystemAdminSchema, data)

        Helper.User_Email_OR_Msisdn_Exist(req.email, req.msisdn)

        role = Role.GetRole(req.role)

        if req.img:

            profile_url, _ = FileHandler.upload_file(req.img, FileFolder.admin_profile(req.email))

        else:
            profile_url = None

        try:
            new_admin = User.CreateUser(req.email, req.msisdn, role)

            if new_admin:
                add_user = Admin(
                    first_name=req.first_name,
                    last_name=req.last_name,
                    country=req.country,
                    state=req.state,
                    user_id=new_admin.id,
                    residence=req.address,
                    gender=req.gender,
                    profile_image=profile_url
                )
                add_user.save(refresh=True)
                Audit.add_audit('Added System Admin', current_user, add_user.to_dict())
                EmailHandler.welcome_mail(new_admin.email, add_user.first_name)
                return {**add_user.to_dict(), "user_id": add_user.user.id}

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def change_profile_image(cls, profile_image, user_id):
        if not profile_image:
            raise CustomException(message="User profile image is required")

        user: User = User.GetUser(user_id)

        if not user.admins:
            raise CustomException(message="Admin does not exist", status_code=404)

        profile_url, _ = FileHandler.upload_file(profile_image, FileFolder.admin_profile(user.email))

        user.admins.profile_image = profile_url
        db.session.commit()
        return "Profile Image has been updated successfully"

    @classmethod
    def get_all_admin(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _admin = Admin.query.order_by(desc(Admin.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _admin.total
        results = [item for item in _admin.items]

        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_deactivated_admins": len([x for x in results if x.user.isDeactivated]),
                "num_of_active_admins": len([x for x in results if not x.user.isDeactivated]),
                "num_of_admins": len(results),
                "admins": [{
                    **res.to_dict(),
                    "user_id": res.user.id,
                    **(res.user.as_dict() if res.user else {}),
                    "role_name": ' '.join(res.user.roles.name.split('_')) if res.user.roles else None
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_admin(cls, user_id, data):
        user: User = User.GetUser(user_id)

        if not user.admins:
            raise CustomException(message="Admin does not exist", status_code=404)

        gender = data.get('gender')
        role = data.get('role')
        if role:
            user.role_id = role
        if gender:
            user.admins.gender = gender
        user.admins.update_table(data)
        Audit.add_audit('Updated System Admin Information', current_user, user.admins.to_dict())
        return {**user.admins.to_dict(), "user_id": user.id}

    @classmethod
    def reset_password(cls, user_id):

        user: User = User.GetUser(user_id)

        if not user.admins:
            raise CustomException(message="Admin does not exist", status_code=404)

        Audit.add_audit('Reset System Admin Password', current_user, user.to_dict())

        return Helper.send_otp(user)

    @classmethod
    def deactivate_user(cls, user_id, reason):

        user: User = User.GetUser(user_id)

        if not user.admins:
            raise CustomException(message="Admin does not exist", status_code=404)

        Audit.add_audit('Changed System Admin Account Status ', current_user, user.to_dict())

        return Helper.disable_account(user, reason)

    @classmethod
    def search_admin(cls, args):
        return Helper.look_up_account(Admin, User, args)

    @classmethod
    def get_user(cls, user_id):

        user: User = User.GetUser(user_id)

        if not user.admins:
            raise CustomException(message="Admin does not exist", status_code=404)

        _user = Helper.get_user(Admin, user.admins.id)
        file_path = FileFolder.admin_profile(user.email)

        return {
            **_user.to_dict(),
            **_user.user.as_dict(),
            "user_id": user.id,
            "profile_image": FileHandler.get_file_url(file_path),
            "role_name": _user.user.roles.name,
            "permissions": [x.name for x in _user.user.roles.permissions] if _user.user.roles else None
        }
