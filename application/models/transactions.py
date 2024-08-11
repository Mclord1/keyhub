import datetime

from application import db
from application.Mixins.GenericMixins import GenericMixin
from application.module import current_user
from exceptions.custom_exception import CustomException


class Transaction(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=True)
    reference = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"), nullable=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id', ondelete="CASCADE"), nullable=True)
    plan_id = db.Column(db.Integer, nullable=True)
    channel = db.Column(db.String(200), nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    fees = db.Column(db.Integer, nullable=True)
    card_authorization_code = db.Column(db.String(200), nullable=True)
    card_bin = db.Column(db.String(20), nullable=True)
    card_last4 = db.Column(db.String(10), nullable=True)
    card_exp_month = db.Column(db.String(10), nullable=True)
    card_exp_year = db.Column(db.String(50), nullable=True)
    card_type = db.Column(db.String(100), nullable=True)
    card_bank = db.Column(db.String(100), nullable=True)
    card_country_code = db.Column(db.String(50), nullable=True)
    card_brand = db.Column(db.String(100), nullable=True)
    purpose = db.Column(db.String(100), nullable=True)
    card_reusable = db.Column(db.Boolean, nullable=True)
    card_signature = db.Column(db.String(200), nullable=True)
    customer_id = db.Column(db.Integer, nullable=True)
    customer_name = db.Column(db.String(150), nullable=True)
    customer_email = db.Column(db.String(150), nullable=True)
    customer_phone = db.Column(db.String(120), nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    schools = db.relationship("School", back_populates='transactions')
    subscriptions = db.relationship("Subscription", back_populates='transactions')

    def __init__(self, data, school=None, subscriptions=None):
        self.status = data.get('status')
        self.reference = data.get('reference')
        self.amount = data.get('amount')
        metadata = data.get('metadata')
        self.subscription_id = subscriptions.id if subscriptions else None
        self.school_id = school.id if school else None
        self.plan_id = metadata.get('planId')
        self.channel = data.get('channel')
        self.completed_date = datetime.datetime.now() if self.status == "success" else None
        self.currency = data.get('currency')
        self.ip_address = data.get('ip_address')
        self.fees = data.get('fees')
        self.purpose = data.get('purpose')
        authorization = data.get('authorization', {})
        self.card_authorization_code = authorization.get('authorization_code')
        self.card_bin = authorization.get('bin')
        self.card_last4 = authorization.get('last4')
        self.card_exp_month = authorization.get('exp_month')
        self.card_exp_year = authorization.get('exp_year')
        self.card_type = authorization.get('card_type')
        self.card_bank = authorization.get('bank')
        self.card_country_code = authorization.get('country_code')
        self.card_brand = authorization.get('brand')
        self.card_reusable = authorization.get('reusable')
        self.card_signature = authorization.get('signature')
        customer = data.get('customer')
        self.customer_id = customer.get('id')
        self.customer_name = f"{customer.get('first_name')} {customer.get('last_name')}"
        self.customer_email = customer.get('email')
        self.customer_phone = customer.get('phone')

    @classmethod
    def GetSchoolTransaction(cls, transaction_id):

        if not current_user.admins and not current_user.managers:
            raise CustomException(message="Only school admin or system admin can access transaction", status_code=401)

        _transaction = Transaction.query.filter(Transaction.id == transaction_id)

        if not current_user.admins and current_user.managers:
            _transaction.filter(Transaction.school_id == current_user.managers.school_id)

        _transaction = _transaction.first()
        if not _transaction:
            raise CustomException(message="Transaction does not exist", status_code=404)

        return _transaction
