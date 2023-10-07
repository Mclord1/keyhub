from typing import TypeVar

from sqlalchemy import BigInteger, func
from sqlalchemy.ext.declarative import declared_attr

from application import db

T = TypeVar('T')


class GenericMixin(object):

    def __init__(cls, **kwargs):
        super(GenericMixin, cls).__init__(**kwargs)

    @declared_attr
    def created_at(cls):
        return db.Column(BigInteger, default=func.extract('epoch', func.current_timestamp()))

    @declared_attr
    def last_updated(cls):
        return db.Column(BigInteger, default=func.extract('epoch', func.current_timestamp()),
                         onupdate=func.extract('epoch', func.current_timestamp()))

    def to_dict(cls, add_filter=True):
        return {'user_id' if column.name == 'id' and add_filter else column.name: getattr(cls, column.name) for
                column in cls.__table__.columns if column.name != 'user_id'}

    def update_table(cls, updates: dict):
        valid_attributes = [column.key for column in cls.__table__.columns]

        valid_updates = {key: value for key, value in updates.items() if key in valid_attributes}

        for key, value in valid_updates.items():
            setattr(cls, key, value)

        db.session.commit()
        return valid_updates

    def save(cls, refresh: bool = False):
        db.session.add(cls)
        db.session.commit()

        if refresh:
            db.session.refresh(cls)
