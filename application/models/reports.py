from application import db
from application.Mixins.GenericMixins import GenericMixin


class Report(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON(none_as_null=True), nullable=True)
    schools = db.relationship("School", back_populates='reports')
