from enum import Enum

from submodule_util_3kle.util.custom_exception.custom_exception import CustomException, ExceptionCode

from app import db
from app.Mixins.GenericMixins import GenericMixin


class ChannelEnum(Enum):
    TRIKLE_C2C = "3kle-c2c"
    TRIKLE_A2A = "3kle-a2a"
    TRIKLE_B2C = "3kle-b2c"
    TRIKLE_C2B = "3kle-c2b"
    TRIKLE_BILL = "3kle-bill"
    TRIKLE_POS = "3kle-pos"
    SPEND_SAVE = "spend-save"
    AUTO_INVEST = "auto-invest"
    EASY_RETIREMENT = "easy-retirement"
    FIXED_SAVINGS = "fixed-savings"
    EMERGENCY_SAVINGS = "emergency-savings"
    PEER_TO_PEER_PERSONAL = "peer-to-peer-personal"
    NQR = "NQR"
    SELF_TRADE = "self-trade"
    FAMILY_PLUS = "family-plus"
    TRIKLE_PAY = "3kle-pay"
    FOREX_SAVINGS = "forex-savings"
    USSD = "ussd"
    PEER_TO_PEER_BUSINESS = "peer-to-peer-business"
    OVERDRAFT = "overdraft"
    BUDGET_SPENDING = "budget-spending"
    GOAL_SAVINGS = "goal-savings"
    ROUND_UPS = "round-ups"
    TRIKLE_LENDING = "3kle-lending"
    CARDLESS = "cardless"
    GROUP_SAVINGS = "group-savings"
    LINK_EXTERNAL_BANK = "link-external-bank"
    BILL_PAYMENT = "bill-payment"
    QUICK_LOAN = "quick-loan"
    SEND_MONEY = "send-money"


class Channel(GenericMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    transactions = db.relationship("Transaction", foreign_keys="Transaction.channel_id", back_populates="channels")
    log_transaction = db.relationship("TransactionLog", back_populates="channels")

    @staticmethod
    def get_channel_name(channel_id: int):
        """Get name of channel

        :param channel_id: channel id to find
        :return: name of the channel if it exists, if not an exception is thrown
        """
        channel: Channel = Channel.query.filter_by(id=channel_id).first()
        if channel is None:
            raise CustomException(ExceptionCode.CHANNEL_NOT_FOUND)
        return channel.name

    @staticmethod
    def get_channel_id(channel_name: str):
        """Get name of channel

        :param channel_name: channel name to find
        :return: name of the channel if it exist, if not an exception is throw
        """
        channel: Channel = Channel.query.filter_by(name=channel_name).first()
        if channel is None:
            raise CustomException(ExceptionCode.CHANNEL_NOT_FOUND)
        return channel.id

    @staticmethod
    def get_channels(names: list):
        return Channel.query.filter(Channel.name.in_(names)).all()

    def check_channel_is_active(self):
        return self.active
