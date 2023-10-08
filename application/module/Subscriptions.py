from collections import Counter

from . import *
from ..models.subscription import SubscriptionStatusEnum


class SubscriptionModel:

    @classmethod
    def create_plan(cls, data):
        req: SubscriptionSchema = validator.validate_data(SubscriptionSchema, data)

        try:
            create_plan = SubcriptionPlan(
                name=req.name,
                bill_cycle=req.billing_cycle,
                description=req.description,
                features=req.features,
                amount=req.amount,
                user=current_user
            )

            create_plan.save(refresh=True)

            return create_plan.to_dict(add_filter=False)

        except IntegrityError:

            db.session.rollback()
            raise CustomException("A subscription plan with name already exist", status_code=400)

    @classmethod
    def update_plan(cls, plan_id, data):
        plan: SubcriptionPlan = SubcriptionPlan.query.filter_by(id=plan_id).first()
        if not plan:
            raise CustomException(ExceptionCode.RESOURCE_NOT_FOUND)
        plan.update_table(data)
        return plan.to_dict(add_filter=False)

    @classmethod
    def delete_plan(cls, plan_id):
        plan: SubcriptionPlan = SubcriptionPlan.query.filter_by(id=plan_id).first()
        if not plan:
            raise CustomException(ExceptionCode.RESOURCE_NOT_FOUND)
        db.session.delete(plan)
        db.session.commit()
        return 'Plan has been deleted successfully'

    @classmethod
    def disable_plan(cls, plan_id):
        plan: SubcriptionPlan = SubcriptionPlan.query.filter_by(id=plan_id).first()
        if not plan:
            raise CustomException(ExceptionCode.RESOURCE_NOT_FOUND)
        plan.isActive = not plan.isActive
        db.session.commit()
        return f'Plan status has been set to {plan.isActive}'

    @classmethod
    def get_subscriptions(cls):
        query_plans = SubcriptionPlan.query.all()
        subscriptions = Subscription.query.all()
        status_counter = Counter([x.status.value for x in subscriptions])
        plan_name = Counter(
            [x.subscription_plan.name for x in subscriptions if x.status.value == SubscriptionStatusEnum.ACTIVE.value])

        return {
            "plans": [x.to_dict(add_filter=False) for x in query_plans],
            "subscriptions": [x.to_dict(add_filter=False) for x in subscriptions],
            "active_plans": status_counter[SubscriptionStatusEnum.ACTIVE.value],
            "paused_plans": status_counter[SubscriptionStatusEnum.PAUSED.value],
            "expired_plans": status_counter[SubscriptionStatusEnum.EXPIRED.value],
            "cancelled_plans": status_counter[SubscriptionStatusEnum.CANCELLED.value],
            "subcription_distribution": {
                "total_schools": status_counter[SubscriptionStatusEnum.ACTIVE.value],
            },
            "subcription_statistics": [],
        }
