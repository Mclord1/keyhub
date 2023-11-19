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
            Audit.add_audit('Add School Learning group', current_user, new_group.to_dict(add_filter=False))
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
            Audit.add_audit("Deactivate learning group" if _group.isDeactivated else "Activate learning group ", current_user, _group.to_dict(add_filter=False))
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
            Audit.add_audit('Delete Learning group', current_user, _group.to_dict(add_filter=False))
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
            Audit.add_audit('Update Learning group information', current_user, _group.to_dict(add_filter=False))
            return _group.to_dict(add_filter=False)
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def add_comment(cls, school_id, group_id, comment):
        group = LearningGroup.GetLearningGroupID(school_id, group_id)
        new_comment = LearningGroupComment(learning_group_id=group.id, user_id=current_user.id, comment=comment)
        new_comment.save(refresh=True)
        return "Comment has been added successfully"

    @classmethod
    def get_comments(cls, school_id, group_id):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
        return [
            {
                **x.to_dict(add_filter=False),
                "commented_by": x.user.email,

            }
            for x in group.learning_group_comments]

    @classmethod
    def remove_comment(cls, group_id, comment_id):
        comments: LearningGroupComment = LearningGroupComment.query.filter_by(learning_group_id=group_id, id=comment_id).first()
        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers or current_user.id != comments.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        comments.delete()
        return "Comment has been deleted successfully"

    @classmethod
    def add_file(cls, school_id, group_id, file):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        file_path, file_name = FileFolder.learning_group_file(group.schools.name, group.name)

        profile_url = FileHandler.upload_file(file, file_path)

        new_file = LearningGroupFile(learning_group_id=group.id, file_name=file_name, file_url=profile_url, file_path=file_path, user_id=current_user.id)
        new_file.save()
        return "File has been added successfully"

    @classmethod
    def get_files(cls, school_id, group_id):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
        return [
            {
                **x.to_dict(add_filter=False),
                "uploaded_by": x.user.email,

            }
            for x in group.learning_group_files]

    @classmethod
    def remove_file(cls, group_id, file_id):
        _files: LearningGroupFile = LearningGroupFile.query.filter_by(learning_group_id=group_id, id=file_id).first()
        if not _files:
            raise CustomException(message="File not found", status_code=404)

        if not current_user.managers or current_user.id != _files.user_id:
            if not current_user.admins :
                raise CustomException(message="Only File author or admin can delete this File", status_code=400)

        FileHandler.delete_file(_files.file_path)
        _files.delete()
        return "File has been deleted successfully"
