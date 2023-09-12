from application import db
from application.Mixins.GenericMixins import GenericMixin


class Admin(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    country = db.Column(db.String(250), nullable=True)
    state = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='admins')
    residence = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(150), nullable=True)
    audits = db.relationship("Audit", back_populates='admins')
