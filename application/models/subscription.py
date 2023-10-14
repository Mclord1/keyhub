import enum

from application import db
from application.Mixins.GenericMixins import GenericMixin


class SubscriptionStatusEnum(enum.Enum):
    CANCELLED = "cancelled"
    PROCESSING = "processing"
    FAILED = "failed"
    DECLINED = "declined"
    PAUSED = "paused"
    ACTIVE = "active"
    EXPIRED = "expired"


class SubcriptionPlan(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True, unique=True)
    bill_cycle = db.Column(db.String(350), nullable=True)
    description = db.Column(db.String(350), nullable=True)
    features = db.Column(db.JSON, nullable=True)
    amount = db.Column(db.String(250), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    subscriptions = db.relationship("Subscription", back_populates='subscription_plan', cascade="all, delete-orphan")
    user = db.relationship("User", back_populates='subscription_plan')


class Subscription(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subcription_plan.id', ondelete="CASCADE"), nullable=False)
    amount = db.Column(db.Float, nullable=True, default=0)
    recurring = db.Column(db.Boolean, default=False)
    next_billing_date = db.Column(db.DateTime, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    payment_type = db.Column(db.String(250), nullable=True)
    action = db.Column(db.JSON, nullable=True)
    status = db.Column(db.Enum(SubscriptionStatusEnum, nullable=True,
                               values_callable=lambda x: [str(member.value) for member in SubscriptionStatusEnum]),
                       default=SubscriptionStatusEnum.ACTIVE.value)
    schools = db.relationship("School", back_populates='subscriptions')
    subscription_plan = db.relationship("SubcriptionPlan", back_populates='subscriptions')
