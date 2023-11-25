from collections import Counter

from . import *
from ..models.subscription import SubscriptionStatusEnum


class PlanModel:

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
            Audit.add_audit('Added Subscription Plan', current_user, create_plan.to_dict(add_filter=False))

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
        Audit.add_audit('Updated Subscription Plan', current_user, plan.to_dict(add_filter=False))
        return plan.to_dict(add_filter=False)

    @classmethod
    def delete_plan(cls, plan_id):
        plan: SubcriptionPlan = SubcriptionPlan.query.filter_by(id=plan_id).first()
        if not plan:
            raise CustomException(ExceptionCode.RESOURCE_NOT_FOUND)

        try:
            Audit.add_audit('Deleted Subscription Plan', current_user, plan.to_dict(add_filter=False))
            db.session.delete(plan)
            db.session.commit()
            return 'Plan has been deleted successfully'
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def list_plans(cls):
        plans = SubcriptionPlan.query.all()
        return [{**x.to_dict(add_filter=False), "created_by": x.user.email} for x in plans]

    @classmethod
    def disable_plan(cls, plan_id):
        plan: SubcriptionPlan = SubcriptionPlan.query.filter_by(id=plan_id).first()
        if not plan:
            raise CustomException(ExceptionCode.RESOURCE_NOT_FOUND)
        try:
            plan.isActive = not plan.isActive
            db.session.commit()
            Audit.add_audit('Deactivated Subscription Plan' if not plan.isActive else 'Activate Subscription Plan', current_user, plan.to_dict(add_filter=False))
            return f'Plan status has been set to {plan.isActive}'
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def get_subscriptions(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        subscriptions = Subscription.query.order_by(desc(Subscription.created_at)).paginate(page=page,
                                                                                            per_page=per_page,
                                                                                            error_out=False)
        total_items = subscriptions.total
        results: List[Subscription] = [item for item in subscriptions.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "subscriptions": [{
                    **res.to_dict(add_filter=False),
                    "status": res.status.value,
                    "school_name": res.schools.name,
                    "plan_name": res.subscription_plan.name
                } for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_subscription_page_info(cls):
        query_plans = SubcriptionPlan.query.all()
        subscriptions = Subscription.query.all()
        status_counter = Counter([x.status.value for x in subscriptions])
        plan_distribution = Counter(
            [x.subscription_plan.name for x in subscriptions if x.status.value == SubscriptionStatusEnum.ACTIVE.value])

        convert_to_date = lambda x: datetime.datetime.fromtimestamp(x)  # noqa

        # subscription_monthly_stat = db.session.query(
        #     func.DATE_TRUNC('month', convert_to_date(1696841797)).label('year_month'),
        #     SubcriptionPlan.created_at,
        #     func.count().label('subscription_count')
        # ).group_by(SubcriptionPlan.id).all()

        return {
            "plans": [x.to_dict(add_filter=False) for x in query_plans],
            "active_plans": status_counter[SubscriptionStatusEnum.ACTIVE.value],
            "paused_plans": status_counter[SubscriptionStatusEnum.PAUSED.value],
            "expired_plans": status_counter[SubscriptionStatusEnum.EXPIRED.value],
            "cancelled_plans": status_counter[SubscriptionStatusEnum.CANCELLED.value],
            "subcription_distribution": {
                "total_schools": status_counter[SubscriptionStatusEnum.ACTIVE.value],
                "plan_distribution": plan_distribution
            },
            "subcription_statistics": []
        }
