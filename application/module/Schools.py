from . import *


class SchoolModel:

    @classmethod
    def list_all_schools(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _school: School = School.query.paginate(page=page, per_page=per_page, error_out=False)
        total_items = _school.total
        results = [item.to_dict() for item in _school.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": results
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def view_school_info(cls, school_id):
        _school: School = School.GetSchool(school_id)
        return _school.to_dict()

    @classmethod
    def add_school(cls, data):
        school_name = data['name']
        email = data['email']
        msisdn = data['msisdn']
        reg_number = data['reg_number']

        _school: School = School.query.filter(
            (School.name == school_name) |
            (School.email == email) |
            (School.msisdn == msisdn) |
            (School.reg_number == reg_number)
        ).first()

        if _school:
            raise CustomException(message="Either name or email or phone number or reg number already exist")

        add_school = School(**data)
        add_school.save(refresh=True)
        return f"The school {add_school.name} has been added successfully"
