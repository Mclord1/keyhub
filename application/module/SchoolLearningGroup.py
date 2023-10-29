from . import *
from ..Schema.school import LearningGroupSchema


class SchoolLearningGroupsModel:

    @classmethod
    def list_all_groups(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _group = LearningGroup.query.filter(LearningGroup.school_id == school_id).order_by(
            desc(LearningGroup.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _group.total
        results = [item for item in _group.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "total_active": len([x for x in results if not x.isDeactivated]),
                "total_inactive": len([x for x in results if x.isDeactivated]),
                "groups": [{
                    **res.to_dict(add_filter=False),
                    "created_by": res.user.email if res.user else None,
                    "creator_name": f'{res.user.admins.first_name} {res.user.admins.last_name}' if res.user else None,
                    'students': [x.to_dict() for x in res.students],
                    'teachers': [x.to_dict() for x in res.teachers],
                    'projects': [x.to_dict(add_filter=False) for x in res.projects],
                }
                    for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_group_detail(cls, school_id, group_id):
        _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        return {
            'name': _group.name,
            'created_on': _group.created_at,
            'created_by': _group.user.email if _group.user else None,
            'creator_name': f'{_group.user.admins.first_name} {_group.user.admins.last_name}' if _group.user else None,
            'country': _group.user.admins.country if _group.user else None,
            'description': _group.description,
            'isDeactivated': _group.isDeactivated,
            'students': [x.to_dict() for x in _group.students],
            'teachers': [x.to_dict() for x in _group.teachers],
            'projects': [x.to_dict(add_filter=False) for x in _group.projects],
        }

    @classmethod
    def create_learning_group(cls, data, school_id):
        _school = School.GetSchool(school_id)
        req: LearningGroupSchema = validator.validate_data(LearningGroupSchema, data)

        try:
            new_group = LearningGroup(name=req.name, created_by=current_user.id, description=req.description, schools=_school)
            new_group.save(refresh=True)
            Audit.add_audit('Add School Learning group', current_user, new_group.to_dict())
            return new_group.to_dict(add_filter=False)
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A Learning group with the name already exist")

    @classmethod
    def toggle_school_learning_group_status(cls, school_id, group_id):
        _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        try:
            _group.isDeactivated = not _group.isDeactivated
            db.session.commit()
            Audit.add_audit("Deactivate learning group" if _group.isDeactivated else "Activate learning group ", current_user, _group.to_dict())
            return f"The Group has been deactivated" if _group.isDeactivated else "The Group has been activated"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def delete_group(cls, school_id, group_id):
        _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        if _group.students or _group.teachers or _group.projects:
            raise CustomException(message="There are users associated to this school group", status_code=500)

        try:

            db.session.commit()
            db.session.delete(_group)
            Audit.add_audit('Delete Learning group', current_user, _group.to_dict())
            db.session.commit()
            return "The group has been deleted"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def update_group(cls, school_id, group_id, name, description):
        try:
            _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
            if name:
                _group.name = name
            if description:
                _group.description = description
            db.session.commit()
            Audit.add_audit('Update Learning group information', current_user, _group.to_dict())
            return _group.to_dict(add_filter=False)
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
