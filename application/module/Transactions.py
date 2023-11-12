from . import *
from ..models.subscription import SubscriptionStatusEnum


class TransactionModel:

    @classmethod
    def get_transactions(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)

        if not current_user.admins and not current_user.managers:
            raise CustomException(message="Only school admin or system admin can access transaction", status_code=401)

        query = Transaction.query

        if not current_user.admins and current_user.managers:
            query.filter(Transaction.school_id == current_user.managers.school_id)

        _transactions = query.order_by(desc(Transaction.created_at)).paginate(page=page, per_page=per_page, error_out=False)

        total_items = _transactions.total
        results: List[Transaction] = [item for item in _transactions.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "num_of_transactions": len(results),
                "num_of_completed_transactions": len([x for x in results if x.status != "success"]),
                "num_of_pending_transactions": len([x for x in results if x.status == "success"]),
                "transactions": [{
                    "created": trans.created_at,
                    "amount": trans.amount / 100,
                    "payer": trans.schools.name,
                    "purpose": trans.purpose,
                    "status": trans.status,
                    "currency": trans.currency,
                    "id": trans.id,
                } for trans in results]
            }

        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_single_transaction(cls, transaction_id):

        _transaction: Transaction = Transaction.GetSchoolTransaction(transaction_id)
        print(_transaction.schools.transactions)
        return {
            **_transaction.to_dict(add_filter=True),
            "payer": _transaction.schools.name,
            "phone_number": _transaction.schools.msisdn,
            "amount": _transaction.amount / 100,
            "total_transaction_volume": len(_transaction.schools.transactions),
            "total_transaction_pending": len([x for x in _transaction.schools.transactions if x.status == "processing"]),
            "total_transaction_completed": len([x for x in _transaction.schools.transactions if x.status == "success"]),
        }

    @classmethod
    def mark_as_completed(cls, transaction_id):
        _transaction: Transaction = Transaction.GetSchoolTransaction(transaction_id)

        if not current_user.admins:
            raise CustomException(message="Only System admin can perform this action", status_code=400)

        if _transaction.subscriptions:
            if not any(x for x in _transaction.schools.subscriptions if x.status == SubscriptionStatusEnum.ACTIVE.value):
                _transaction.subscriptions.status = SubscriptionStatusEnum.ACTIVE.value

        _transaction.status = "success"
        _transaction.completed_date = datetime.datetime.now()

        db.session.commit()

    @classmethod
    def mark_as_cancelled(cls, transaction_id):
        _transaction = Transaction.GetSchoolTransaction(transaction_id)

        if not current_user.admins:
            raise CustomException(message="Only System admin can perform this action", status_code=400)

        if _transaction.subscriptions:
            _transaction.subscriptions.status = SubscriptionStatusEnum.CANCELLED.value

        _transaction.status = "cancelled"
        db.session.commit()

    @classmethod
    def search_school_transaction(cls, args):

        if not current_user.admins and not current_user.managers:
            raise CustomException(message="Only school admin or system admin can access transaction", status_code=401)

        query = Transaction.query.filter(
            (Transaction.customer_name.ilike(f'%{args}%') | Transaction.purpose.ilike(f'%{args}%'))
        )

        if not current_user.admins and current_user.managers:
            query.filter(Transaction.school_id == current_user.managers.school_id)

        result = [x.to_dict(add_filter=False) for x in query.all()]

        return result or []
