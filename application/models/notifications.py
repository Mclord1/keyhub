from sqlalchemy import JSON

from application import db
from application.Mixins.GenericMixins import GenericMixin


class Notification(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    data = db.Column(JSON, default={}, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), nullable=True)
    user = db.relationship("User", back_populates='notifications')

    @classmethod
    def send_push_notification(cls, users, message, category=None, data=None):
        # TODO :: Add celery background task
        try:
            for user_id in users:
                new_notification = Notification(user_id=user_id, message=message, data=data, category=category)
                db.session.add(new_notification)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
