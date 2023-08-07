from app import db
from app.Enums.Enums import ReferralStatusEnum
from app.Mixins.GenericMixins import GenericMixin


class Referral(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    referral_code = db.Column(db.String(250), nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(ReferralStatusEnum, nullable=True, values_callable=lambda x: [str(member.value) for member in ReferralStatusEnum]))
    user = db.relationship("User", back_populates='referrals')
