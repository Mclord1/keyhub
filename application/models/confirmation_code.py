from application import db
from application.Mixins.GenericMixins import GenericMixin


class ConfirmationCode(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    code = db.Column(db.String(150), nullable=True)
    msisdn = db.Column(db.String(150), nullable=True)
    counter = db.Column(db.Integer, nullable=True, default=0)
    expiration = db.Column(db.DateTime, nullable=True)
    user = db.relationship("User", back_populates='confirmation_codes')
