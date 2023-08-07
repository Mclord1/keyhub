from app import db

from app.Enums.Enums import *
from app.Mixins.GenericMixins import GenericMixin


class Verification(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dob = db.Column(db.DateTime, nullable=True)
    driving_license = db.Column(db.String(32), nullable=True)
    health_insurance = db.Column(db.String(150), nullable=True)
    marital_status = db.Column(db.String(150), nullable=True)
    national_id = db.Column(db.String(32), nullable=True)
    nationality = db.Column(db.String(32), nullable=True)
    firstname = db.Column(db.String(100), nullable=True)
    surname = db.Column(db.String(100), nullable=True)
    other_names = db.Column(db.String(256), nullable=True)
    full_name = db.Column(db.String(250), nullable=True)
    passport = db.Column(db.String(32), nullable=True)
    ssn = db.Column(db.String(32), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    error_reason = db.Column(db.String(255), nullable=True)
    business_name = db.Column(db.String(), nullable=True)
    cac_number = db.Column(db.String(), nullable=True)
    docTypeUrl = db.Column(db.String(550), nullable=True)  # contains url for kyc
    verification_state = db.Column(db.Enum(VerificationEnum, values_callable=lambda x: [str(member.value) for member in VerificationEnum]), nullable=False)
    check_type = db.Column(db.Enum(VerificationTypeEnum, values_callable=lambda x: [str(member.value) for member in VerificationTypeEnum]), nullable=False)
    user = db.relationship("User", back_populates='verifications')
