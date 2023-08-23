import enum

from application import db
from application.Mixins.GenericMixins import GenericMixin


class SubscriptionStatusEnum(enum.Enum):
    CANCELLED = "cancelled"
    PROCESSING = "processing"
    FAILED = "failed"
    DECLINED = "declined"
    ACTIVE = "active"
    EXPIRED = "expired"


class SubscriptionPlanEnum(enum.Enum):
    STARTER = "starter"
    GOLD = "gold"
    SILVER = "silver"


class SubcriptionPlan(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    subscriptions = db.relationship("Subscription", back_populates='subscription_plan')


class Subscription(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subcription_plan.id'), nullable=False)
    amount = db.Column(db.Float, nullable=True, default=0)
    recurring = db.Column(db.Boolean, default=False)
    next_billing_date = db.Column(db.DateTime, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    payment_type = db.Column(db.String(250), nullable=True)
    action = db.Column(db.JSON, nullable=True)
    status = db.Column(db.Enum(SubscriptionStatusEnum, nullable=True, values_callable=lambda x: [str(member.value) for member in SubscriptionStatusEnum]),
                       default=SubscriptionStatusEnum.ACTIVE.value)
    schools = db.relationship("School", back_populates='subscriptions')
    subscription_plan = db.relationship("SubcriptionPlan", back_populates='subscriptions')
