from application import db
from application.Mixins.GenericMixins import GenericMixin


class Message(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.Text, nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_accepted = db.Column(db.Boolean, default=True)
    is_read = db.Column(db.Boolean, default=False)
    is_school_convo = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')

