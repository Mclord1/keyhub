from application import db
from application.Mixins.GenericMixins import GenericMixin


class SME(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete='CASCADE'), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    contact_telephone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    company_name = db.Column(db.String(200), nullable=True, unique=True)
    registered_address = db.Column(db.Text, nullable=True)
    area_of_expertise = db.Column(db.Text, nullable=True)
    nin_certificate = db.Column(db.Boolean, nullable=False)

    # Define a one-to-many relationship between SMEs and schools
    schools = db.relationship("School", back_populates="smes")


class Keywords(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
