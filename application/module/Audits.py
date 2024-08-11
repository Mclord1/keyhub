from . import *


class AuditModel:

    @classmethod
    def list_audits(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _audit = Audit.query.order_by(desc(Audit.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _audit.total
        results = [item for item in _audit.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "audits": [{
                    'id': res.id,
                    'created_on': res.created_at,
                    'action': res.action,
                    "created_by": res.user.email if res.user else None,
                    "creator_name": User.GetUserFullName(res.user.id),
                }
                    for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_audit_detail(cls, audit_id):
        _audit: Audit = Audit.query.filter(Audit.id == audit_id).first()

        if not _audit:
            raise CustomException(message="Audit not found", status_code=404)

        return {
            'id': _audit.id,
            'action': _audit.action,
            'created_on': _audit.created_at,
            'created_by': _audit.user.email,
            'data': _audit.data,
            'creator_name': User.GetUserFullName(_audit.user_id),

        }
