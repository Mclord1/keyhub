from application import db
from application.Mixins.GenericMixins import GenericMixin


class TransactionModel(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=True, unique=True)
    