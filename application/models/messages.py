from application import db
from application.Mixins.GenericMixins import GenericMixin


class Message(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    room = db.relationship('User', foreign_keys=[receiver_id])
