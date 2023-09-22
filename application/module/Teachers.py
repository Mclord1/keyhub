from . import *


class Teacher:

    @classmethod
    def get_all_teachers(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        role = Role.GetRoleByName('teacher')
        _teachers = User.query.filter_by(role_id=role.id).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _teachers.total
        results = [item.teachers.to_dict() | item.to_dict() for item in _teachers.items]
        total_pages = (total_items - 1) // per_page + 1

        for item in results:
            item.pop("password", None)
            item.pop("id", None)

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": results
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def update_information(cls, user_id, data):
        _user: User = User.GetUser(user_id)
        _user.admins.update_table(data)
        return _user.admins.to_dict()

    @classmethod
    def add_teacher(cls):
        pass

    @classmethod
    def search_teachers(cls):
        pass
