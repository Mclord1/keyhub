from sqlalchemy import UniqueConstraint, BigInteger, func, and_

from app import db
from app.Mixins.GenericMixins import GenericMixin
import enum

from submodule_util_3kle.util.custom_exception.custom_exception import CustomException, ExceptionCode


class AccountTypeEnum(enum.Enum):
    PERSONAL = 'PERSONAL'
    BUSINESS = 'BUSINESS'


class Account(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_number = db.Column(db.Integer, nullable=True)
    account_type = db.Column(db.Enum(AccountTypeEnum, nullable=True, values_callable=lambda x: [str(member.value) for member in AccountTypeEnum]))
    account_balance = db.Column(db.Integer, default=0.0)
    currency = db.Column(db.String(50), default="NGN")
    is_active = db.Column(db.Boolean, default=True)
    activation_status_changed_on = db.Column(BigInteger, nullable=True)
    activation_status_changed_by = db.Column(db.String(250), nullable=True)

    # Unique constraint to ensure each user can have only one personal and one business account
    __table_args__ = (UniqueConstraint('user_id', 'account_type', name='unique_user_account_type'),)

    sent_transactions = db.relationship("Transaction", foreign_keys="Transaction.sender_account_id", back_populates="sender_account")
    received_transactions = db.relationship("Transaction", foreign_keys="Transaction.receiver_account_id", back_populates="receiver_account")

    user = db.relationship("User", back_populates='accounts')

    business = db.relationship("Business", backref='account', lazy=True, cascade="all,delete")

    @staticmethod
    def get_personal_account(user_id):
        account = Account.query.filter_by(user_id=user_id, account_type=AccountTypeEnum.PERSONAL.value).first()

        if not account:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        if not account.is_active:
            raise CustomException(ExceptionCode.ACCOUNT_INACTIVE)

        return account

    @staticmethod
    def get_business_account(user_id):
        account = Account.query.filter_by(user_id=user_id, account_type=AccountTypeEnum.BUSINESS.value).first()

        if not account:
            raise CustomException(ExceptionCode.ACCOUNT_NOT_FOUND)

        if not account.is_active:
            raise CustomException(ExceptionCode.ACCOUNT_INACTIVE)

        return account

    def balance(self, filter_date=None):
        from app.models.transaction import Transaction, TransactionStatusEnum

        """
            In this optimized function, we use a single query with case statements to calculate the sums of 
            lodgements, disbursements, and fees based on different conditions. The case statement acts as a 
            conditional aggregation, and we use the func.sum() function to compute the sums. The final balance is 
            then calculated by subtracting the disbursements and fees from the lodgements.
            This approach reduces the number of database queries to just one, resulting in
             improved performance, especially for large datasets.
        """

        # Calculate the sums of lodgements, disbursements, and fees using a single query
        from sqlalchemy import case, func, not_

        query = db.session.query(
            func.sum(case([(and_(Transaction.receiver_account_id == self.id, Transaction.status == TransactionStatusEnum.COMPLETED.value), Transaction.amount)], else_=0)
                     ).label(
                "lodgements_sum"),
            func.sum(case([(
                and_(Transaction.sender_account_id == self.id, Transaction.status.in_(
                    [TransactionStatusEnum.PROCESSING.value, TransactionStatusEnum.PENDING.value, TransactionStatusEnum.COMPLETED.value])), Transaction.amount)], else_=0)
            ).label("disbursements_sum"),
            func.sum(case([(
                and_(Transaction.sender_account_id == self.id, Transaction.status.in_(
                    [TransactionStatusEnum.PROCESSING.value, TransactionStatusEnum.PENDING.value, TransactionStatusEnum.COMPLETED.value]),
                     not_(Transaction.fee.is_(None))), Transaction.fee)], else_=0)).label("fees_sum"),
        )

        if filter_date:
            query = query.filter(Transaction.created <= filter_date)

        # execute the query
        result = query.first()
        lodgements_total = result.lodgements_sum or 0
        disbursements_total = result.disbursements_sum or 0
        fees_total = result.fees_sum or 0

        return lodgements_total - disbursements_total - fees_total
