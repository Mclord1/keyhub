from datetime import datetime as today_date, date
from typing import Callable

from sqlalchemy import and_

from . import *
from ..Schema.school import SubscribeSchema
from ..models.subscription import SubscriptionStatusEnum


class SubscriptionModel:

    @classmethod
    def create_subscription(cls, school_id, data: dict):

        req: SubscribeSchema = validator.validate_data(SubscribeSchema, data)

        plan: SubcriptionPlan = SubcriptionPlan.query.filter_by(id=req.plan_id).first()

        calc_date: Callable = lambda days: today_date.strptime(str(date.today() + datetime.timedelta(days=days)), "%Y-%m-%d")

        if not plan:
            raise CustomException(ExceptionCode.INVALID_PLAN)

        """
            Check if user has an active subscription running
        """

        sub: Subscription = Subscription.query.filter(
            and_(
                Subscription.status.in_([SubscriptionStatusEnum.ACTIVE.value, SubscriptionStatusEnum.PROCESSING.value]),
                Subscription.school_id == school_id
            )
        ).first()

        is_active = sub.status.value == SubscriptionStatusEnum.ACTIVE.value
        is_processing = sub.status.value == SubscriptionStatusEnum.PROCESSING.value

        if is_processing:
            sub.recurring = req.recurring
            sub.subscription_plan = plan
            db.session.commit()
            return return_json(OutputObj(message="Your plan has been updated.", code=200))


        try:
            if is_active:
                # if subscription already exist
                sub.action = {
                    "plan": plan.id,
                    "type": "change-plan"
                }
                db.session.commit()
                Audit.add_audit('Changed subcription plan', current_user, sub.to_dict(add_filter=False))
                result = f"You have successfully changed your plan to {plan} and it will be effective at the end of your current billing period on {sub.next_billing_date.date()} and you be charged {plan.amount}"
            else:

                table = Subscription(
                    school_id=school_id,
                    subscription_plan=plan,
                    amount=plan.amount,
                    status=SubscriptionStatusEnum.PROCESSING.value,
                    next_billing_date=calc_date(days=int(plan.bill_cycle)),
                    recurring=req.recurring,
                )
                table.save(refresh=True)
                table_info = table.to_dict(add_filter=False)
                table_info['next_billing_date'] = table.next_billing_date.isoformat()
                table_info['status'] = table.status.value
                Audit.add_audit('Added subcription plan', current_user, table_info)
                result = f"Your subscription plan has been created successfully."

            return return_json(OutputObj(message=result, code=200))
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def cancel_subscription(cls, school_id: int):

        sub: Subscription = Subscription.query.filter(
            and_(
                Subscription.status.in_([SubscriptionStatusEnum.ACTIVE.value, SubscriptionStatusEnum.PROCESSING.value]),
                Subscription.school_id == school_id
            )
        ).first()

        if not sub:
            raise CustomException(ExceptionCode.NO_ACTIVE_SUBCRIPTION)

        try:

            if sub.status.value == SubscriptionStatusEnum.PROCESSING.value:
                sub.status = SubscriptionStatusEnum.CANCELLED.value
            else:
                sub.action = {
                    "plan": sub.subscription_plan.name,
                    "type": "cancel"
                }

            db.session.commit()

            result = f"Cancellation on your {sub.subscription_plan.name} plan will be effective at the end of your current billing period on {sub.next_billing_date.date()}."
            table_info = sub.to_dict(add_filter=False)
            table_info['next_billing_date'] = sub.next_billing_date.isoformat()
            table_info['status'] = sub.status.value
            Audit.add_audit('Cancelled subcription plan', current_user, table_info)
            return return_json(OutputObj(message=result, code=200))
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def active_subscription(cls, school_id):
        sub: Subscription = Subscription.query.filter_by(status=SubscriptionStatusEnum.ACTIVE.value, school_id=school_id).first()

        sub: Subscription = Subscription.query.filter(
            and_(
                Subscription.status.in_([SubscriptionStatusEnum.ACTIVE.value, SubscriptionStatusEnum.PROCESSING.value]),
                Subscription.school_id == school_id
            )
        ).first()

        if not sub:
            raise CustomException(ExceptionCode.NO_ACTIVE_SUBCRIPTION)

        result = sub.to_dict()
        to_next_plan = None if not sub.action else sub.action.get('plan')
        to_next_type = None if not sub.action else sub.action.get('type')
        result['end_date'] = sub.end_date.timestamp() if sub.end_date else None
        result['next_billing_date'] = sub.next_billing_date.timestamp()
        result['start_date'] = sub.start_date.timestamp() if sub.start_date else None
        result['cancelled'] = False
        result['status'] = sub.status.value
        result['plan_name'] = sub.subscription_plan.name
        result['features'] = sub.subscription_plan.features

        if to_next_plan and to_next_type == 'cancel':
            result['cancelled'] = True
            result['nextPlan'] = None
        elif to_next_plan and to_next_type == 'change-plan':
            result['nextPlan'] = to_next_plan
        else:
            result['nextPlan'] = result.get('plan', None)

        if result.get('action'):
            del result['action']

        return return_json(OutputObj(message="fetch active subscription", data=result, code=200))

    @classmethod
    def PaymentHistory(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        sub = Subscription.query.filter(Subscription.school_id == school_id).order_by(desc(Subscription.created_at)).paginate(page=page, per_page=per_page,
                                                                                                                              error_out=False)
        total_items = sub.total
        results = [item for item in sub.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": [{
                **x.to_dict(add_filter=False),
                "status": x.status.value,
                "features": x.subscription_plan.features,
                "plan_name": x.subscription_plan.name

            } for x in results]
        }

        return return_json(OutputObj(message="fetch previous payments", data=PaginationSchema(**pagination_data).model_dump(), code=200))
