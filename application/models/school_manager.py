from application import db
from application.Mixins.GenericMixins import GenericMixin


class SchoolManager(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='managers')
    name = db.Column(db.String(250), nullable=True)
    residence = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    designation = db.Column(db.String(250), nullable=True)

    schools = db.relationship("School", back_populates='managers')
